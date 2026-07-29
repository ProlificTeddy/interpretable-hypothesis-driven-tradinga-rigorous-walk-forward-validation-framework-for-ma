from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime
from ..models.hypothesis import Hypothesis
from ..models.walk_forward import WalkForwardResult
from ..models.rl import RLTrainingResult
from ..schemas.report import (
    ValidationStatisticsResponse,
    PerformanceMetricsResponse,
    HypothesisSummaryResponse
)

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_validation_stats(self, hypothesis_id: str, start_date: datetime = None, end_date: datetime = None) -> ValidationStatisticsResponse:
        query = self.db.query(WalkForwardResult).filter(
            WalkForwardResult.hypothesis_id == hypothesis_id
        )

        if start_date:
            query = query.filter(WalkForwardResult.out_of_sample_start >= start_date)
        if end_date:
            query = query.filter(WalkForwardResult.out_of_sample_end <= end_date)

        results = query.all()
        
        if not results:
            raise ValueError("No validation results found")

        # Calculate statistics
        return ValidationStatisticsResponse(
            hypothesis_id=hypothesis_id,
            total_walk_forwards=len(results),
            success_rate=sum(1 for r in results if r.success)/len(results),
            average_profit=sum(r.out_of_sample_profit for r in results)/len(results),
            max_drawdown=min(r.max_drawdown for r in results),
            sharpe_ratio=sum(r.sharpe_ratio for r in results)/len(results),
            sortino_ratio=sum(r.sortino_ratio for r in results)/len(results),
            risk_adjusted_return=sum(r.risk_adjusted_return for r in results)/len(results),
            last_updated=datetime.now()
        )

    def get_performance_metrics(self, hypothesis_id: str, walk_forward_id: str = None) -> PerformanceMetricsResponse:
        if walk_forward_id:
            result = self.db.query(WalkForwardResult).filter(
                WalkForwardResult.id == walk_forward_id
            ).first()
        else:
            result = self.db.query(WalkForwardResult).filter(
                WalkForwardResult.hypothesis_id == hypothesis_id
            ).order_by(WalkForwardResult.out_of_sample_end.desc()).first()

        if not result:
            raise ValueError("No performance data found")

        return PerformanceMetricsResponse(
            walk_forward_id=str(result.id),
            hypothesis_id=hypothesis_id,
            in_sample_performance=result.in_sample_metrics,
            out_of_sample_performance=result.out_of_sample_metrics,
            risk_metrics=result.risk_metrics,
            transaction_cost_impact=result.transaction_cost_analysis
        )

    def get_hypothesis_summary(self, hypothesis_id: str) -> HypothesisSummaryResponse:
        hypothesis = self.db.query(Hypothesis).filter(
            Hypothesis.id == hypothesis_id
        ).first()
        
        if not hypothesis:
            raise ValueError("Hypothesis not found")

        walk_forward = self.db.query(WalkForwardResult).filter(
            WalkForwardResult.hypothesis_id == hypothesis_id
        ).order_by(WalkForwardResult.out_of_sample_end.desc()).first()

        rl_training = self.db.query(RLTrainingResult).filter(
            RLTrainingResult.hypothesis_id == hypothesis_id
        ).order_by(RLTrainingResult.training_metrics['sharpe_ratio'].desc()).first()

        return HypothesisSummaryResponse(
            hypothesis=hypothesis,
            latest_walk_forward=walk_forward,
            best_rl_training=rl_training,
            signal_effectiveness={
                'accuracy': walk_forward.signal_accuracy if walk_forward else 0.0,
                'precision': walk_forward.signal_precision if walk_forward else 0.0
            },
            risk_assessment={
                'value_at_risk': walk_forward.value_at_risk if walk_forward else 0.0,
                'expected_shortfall': walk_forward.expected_shortfall if walk_forward else 0.0
            }
        )