#!/usr/bin/env python3
"""
=== 智能策略学习器 ===

基于机器学习的检索策略选择和优化
这是我们相对于其他RAG方法的核心创新点
"""

import logging
import numpy as np
import pickle
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)


@dataclass
class QueryFeatures:
    """查询特征"""
    complexity_score: float  # 查询复杂度 [0-1]
    entity_count: int       # 实体数量
    token_count: int        # token数量
    question_type: str      # 问题类型 (factual, reasoning, comparison, etc.)
    temporal_indicators: int # 时间指示词数量
    semantic_density: float  # 语义密度
    ambiguity_score: float   # 歧义度评分


@dataclass
class PerformanceMetrics:
    """性能指标"""
    accuracy: float         # 准确性 (F1, EM等)
    latency: float         # 延迟 (秒)
    cost: float            # 成本 (API调用次数等)
    user_satisfaction: float # 用户满意度 [0-1]


@dataclass
class StrategyPerformance:
    """策略性能记录"""
    query_features: QueryFeatures
    strategy_config: Dict[str, float]  # 策略配置 (权重等)
    performance: PerformanceMetrics
    timestamp: float


class QueryComplexityAnalyzer:
    """查询复杂度分析器 - 我们的创新组件"""
    
    def __init__(self):
        self.complexity_indicators = {
            'comparison_words': ['compare', 'versus', 'difference', 'better', 'worse'],
            'reasoning_words': ['why', 'how', 'explain', 'analyze', 'evaluate'],
            'temporal_words': ['when', 'before', 'after', 'during', 'since'],
            'complex_structures': ['not only', 'but also', 'on the other hand']
        }
    
    def analyze_complexity(self, query: str) -> QueryFeatures:
        """分析查询复杂度"""
        tokens = query.lower().split()
        
        # 计算各种复杂度指标
        complexity_score = self._calculate_complexity_score(query, tokens)
        entity_count = self._count_entities(query)
        semantic_density = self._calculate_semantic_density(tokens)
        ambiguity_score = self._calculate_ambiguity_score(query)
        question_type = self._identify_question_type(query)
        temporal_indicators = self._count_temporal_indicators(tokens)
        
        return QueryFeatures(
            complexity_score=complexity_score,
            entity_count=entity_count,
            token_count=len(tokens),
            question_type=question_type,
            temporal_indicators=temporal_indicators,
            semantic_density=semantic_density,
            ambiguity_score=ambiguity_score
        )
    
    def _calculate_complexity_score(self, query: str, tokens: List[str]) -> float:
        """计算复杂度评分"""
        score = 0.0
        
        # 基于长度的复杂度
        length_score = min(len(tokens) / 50.0, 1.0)  # 归一化到[0,1]
        
        # 基于关键词的复杂度
        keyword_score = 0.0
        for category, words in self.complexity_indicators.items():
            matches = sum(1 for word in words if word in query.lower())
            keyword_score += matches * 0.1
        
        # 基于句法结构的复杂度
        syntax_score = 0.0
        if '?' in query:
            syntax_score += 0.1
        if any(word in query.lower() for word in ['and', 'or', 'but']):
            syntax_score += 0.2
        
        score = (length_score * 0.4 + keyword_score * 0.4 + syntax_score * 0.2)
        return min(score, 1.0)
    
    def _count_entities(self, query: str) -> int:
        """简单的实体计数 (可以后续用NER替换)"""
        # 简单启发式：大写开头的词
        tokens = query.split()
        entities = [token for token in tokens if token[0].isupper() and len(token) > 1]
        return len(entities)
    
    def _calculate_semantic_density(self, tokens: List[str]) -> float:
        """计算语义密度"""
        # 简单实现：非停用词比例
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        content_words = [token for token in tokens if token.lower() not in stop_words]
        return len(content_words) / len(tokens) if tokens else 0.0
    
    def _calculate_ambiguity_score(self, query: str) -> float:
        """计算歧义度评分"""
        ambiguous_words = ['it', 'this', 'that', 'they', 'them', 'thing', 'stuff']
        ambiguous_count = sum(1 for word in ambiguous_words if word in query.lower())
        return min(ambiguous_count / 10.0, 1.0)
    
    def _identify_question_type(self, query: str) -> str:
        """识别问题类型"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['what', 'who', 'where', 'when']):
            return 'factual'
        elif any(word in query_lower for word in ['why', 'how', 'explain']):
            return 'reasoning'
        elif any(word in query_lower for word in ['compare', 'difference', 'versus']):
            return 'comparison'
        elif any(word in query_lower for word in ['list', 'enumerate', 'name']):
            return 'enumeration'
        else:
            return 'general'
    
    def _count_temporal_indicators(self, tokens: List[str]) -> int:
        """计算时间指示词数量"""
        temporal_words = self.complexity_indicators['temporal_words']
        return sum(1 for token in tokens if token.lower() in temporal_words)


class IntelligentStrategyLearner:
    """智能策略学习器 - 核心创新组件"""
    
    def __init__(self, config):
        self.config = config
        self.complexity_analyzer = QueryComplexityAnalyzer()
        
        # 机器学习模型
        self.strategy_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.performance_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
        # 历史数据
        self.performance_history: List[StrategyPerformance] = []
        self.is_trained = False
        
        # 默认策略配置
        self.default_strategies = {
            'factual': {'keyword': 0.7, 'dense': 0.2, 'web': 0.1},
            'reasoning': {'keyword': 0.3, 'dense': 0.6, 'web': 0.1},
            'comparison': {'keyword': 0.4, 'dense': 0.4, 'web': 0.2},
            'enumeration': {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},
            'general': {'keyword': 0.4, 'dense': 0.4, 'web': 0.2}
        }
        
        logger.info("IntelligentStrategyLearner 初始化完成")
    
    def predict_optimal_strategy(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """预测最优策略 - 核心方法"""
        # 1. 分析查询特征
        query_features = self.complexity_analyzer.analyze_complexity(query)
        
        # 2. 如果模型已训练，使用ML预测
        if self.is_trained and len(self.performance_history) > 50:
            strategy_config = self._ml_predict_strategy(query_features)
            confidence = self._calculate_prediction_confidence(query_features)
        else:
            # 3. 否则使用基于规则的默认策略
            strategy_config = self._rule_based_strategy(query_features)
            confidence = 0.7  # 中等置信度
        
        # 4. 预测性能
        predicted_performance = self._predict_performance(query_features, strategy_config)
        
        return {
            'strategy_config': strategy_config,
            'query_features': query_features,
            'predicted_performance': predicted_performance,
            'confidence': confidence,
            'reasoning': self._generate_reasoning(query_features, strategy_config)
        }
    
    def _ml_predict_strategy(self, query_features: QueryFeatures) -> Dict[str, float]:
        """使用机器学习预测策略"""
        try:
            # 特征向量化
            feature_vector = self._vectorize_features(query_features)
            feature_vector_scaled = self.scaler.transform([feature_vector])
            
            # 预测各检索器权重
            predictions = self.strategy_predictor.predict(feature_vector_scaled)[0]
            
            # 确保权重和为1且非负
            weights = np.maximum(predictions, 0.01)  # 最小权重0.01
            weights = weights / np.sum(weights)
            
            return {
                'keyword': float(weights[0]),
                'dense': float(weights[1]),
                'web': float(weights[2])
            }
        except Exception as e:
            logger.warning(f"ML预测失败，使用默认策略: {e}")
            return self._rule_based_strategy(query_features)
    
    def _rule_based_strategy(self, query_features: QueryFeatures) -> Dict[str, float]:
        """基于规则的策略选择"""
        base_strategy = self.default_strategies.get(
            query_features.question_type, 
            self.default_strategies['general']
        ).copy()
        
        # 根据复杂度调整
        if query_features.complexity_score > 0.7:
            # 高复杂度查询，增加dense检索权重
            base_strategy['dense'] += 0.1
            base_strategy['keyword'] -= 0.05
            base_strategy['web'] -= 0.05
        
        # 根据实体数量调整
        if query_features.entity_count > 3:
            # 多实体查询，增加keyword检索权重
            base_strategy['keyword'] += 0.1
            base_strategy['dense'] -= 0.05
            base_strategy['web'] -= 0.05
        
        # 归一化权重
        total = sum(base_strategy.values())
        for key in base_strategy:
            base_strategy[key] /= total
        
        return base_strategy
    
    def _vectorize_features(self, features: QueryFeatures) -> List[float]:
        """特征向量化"""
        # 将QueryFeatures转换为数值向量
        question_type_encoding = {
            'factual': [1, 0, 0, 0, 0],
            'reasoning': [0, 1, 0, 0, 0],
            'comparison': [0, 0, 1, 0, 0],
            'enumeration': [0, 0, 0, 1, 0],
            'general': [0, 0, 0, 0, 1]
        }
        
        type_vector = question_type_encoding.get(features.question_type, [0, 0, 0, 0, 1])
        
        return [
            features.complexity_score,
            features.entity_count,
            features.token_count,
            features.temporal_indicators,
            features.semantic_density,
            features.ambiguity_score
        ] + type_vector
    
    def record_performance(self, query: str, strategy_config: Dict[str, float], 
                          performance: PerformanceMetrics):
        """记录策略性能 - 用于学习"""
        query_features = self.complexity_analyzer.analyze_complexity(query)
        
        record = StrategyPerformance(
            query_features=query_features,
            strategy_config=strategy_config,
            performance=performance,
            timestamp=time.time()
        )
        
        self.performance_history.append(record)
        
        # 定期重训练模型
        if len(self.performance_history) % 20 == 0:
            self._retrain_models()
    
    def _retrain_models(self):
        """重新训练模型"""
        if len(self.performance_history) < 10:
            return
        
        try:
            # 准备训练数据
            X = []
            y_strategy = []
            y_performance = []
            
            for record in self.performance_history:
                feature_vector = self._vectorize_features(record.query_features)
                X.append(feature_vector)
                
                strategy_vector = [
                    record.strategy_config['keyword'],
                    record.strategy_config['dense'],
                    record.strategy_config['web']
                ]
                y_strategy.append(strategy_vector)
                
                # 综合性能评分
                perf_score = (
                    record.performance.accuracy * 0.4 +
                    (1 - record.performance.latency / 10.0) * 0.3 +  # 假设10秒为最大延迟
                    record.performance.user_satisfaction * 0.3
                )
                y_performance.append(perf_score)
            
            X = np.array(X)
            y_strategy = np.array(y_strategy)
            y_performance = np.array(y_performance)
            
            # 标准化特征
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            
            # 训练模型
            self.strategy_predictor.fit(X_scaled, y_strategy)
            self.performance_predictor.fit(X_scaled, y_performance)
            
            self.is_trained = True
            logger.info(f"模型重训练完成，使用 {len(self.performance_history)} 条历史数据")
            
        except Exception as e:
            logger.error(f"模型训练失败: {e}")
    
    def save_model(self, path: str):
        """保存模型"""
        model_data = {
            'strategy_predictor': self.strategy_predictor,
            'performance_predictor': self.performance_predictor,
            'scaler': self.scaler,
            'performance_history': self.performance_history,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, path)
        logger.info(f"模型已保存到: {path}")
    
    def load_model(self, path: str):
        """加载模型"""
        try:
            model_data = joblib.load(path)
            self.strategy_predictor = model_data['strategy_predictor']
            self.performance_predictor = model_data['performance_predictor']
            self.scaler = model_data['scaler']
            self.performance_history = model_data['performance_history']
            self.is_trained = model_data['is_trained']
            logger.info(f"模型已从 {path} 加载")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
