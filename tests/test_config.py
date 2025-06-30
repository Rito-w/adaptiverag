#!/usr/bin/env python3
"""
Tests for AdaptiveRAG configuration system
"""

import pytest
import tempfile
import os
from pathlib import Path

from adaptive_rag.config import AdaptiveRAGConfig, save_example_config


class TestAdaptiveRAGConfig:
    """Test AdaptiveRAG configuration system"""
    
    def test_default_config(self):
        """Test default configuration creation"""
        config = AdaptiveRAGConfig()
        
        assert config['dataset_name'] == 'natural_questions'
        assert config['device'] in ['cuda', 'cpu']
        assert config['seed'] == 2024
        assert isinstance(config['retrieval_topk'], int)
    
    def test_config_with_dict(self):
        """Test configuration with dictionary override"""
        config_dict = {
            'dataset_name': 'hotpot_qa',
            'test_sample_num': 100,
            'debug_mode': True
        }
        
        config = AdaptiveRAGConfig(config_dict=config_dict)
        
        assert config['dataset_name'] == 'hotpot_qa'
        assert config['test_sample_num'] == 100
        assert config['debug_mode'] is True
    
    def test_config_with_yaml_file(self):
        """Test configuration with YAML file"""
        yaml_content = """
dataset_name: "trivia_qa"
test_sample_num: 50
retrieval_topk: 10
debug_mode: false
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_file = f.name
        
        try:
            config = AdaptiveRAGConfig(config_file_path=yaml_file)
            
            assert config['dataset_name'] == 'trivia_qa'
            assert config['test_sample_num'] == 50
            assert config['retrieval_topk'] == 10
            assert config['debug_mode'] is False
        finally:
            os.unlink(yaml_file)
    
    def test_config_save(self):
        """Test configuration saving"""
        config = AdaptiveRAGConfig(config_dict={'dataset_name': 'test_dataset'})
        
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = os.path.join(temp_dir, 'test_config.yaml')
            config.save_config(save_path)
            
            assert os.path.exists(save_path)
            
            # Load saved config
            loaded_config = AdaptiveRAGConfig(config_file_path=save_path)
            assert loaded_config['dataset_name'] == 'test_dataset'
    
    def test_save_example_config(self):
        """Test saving example configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            example_path = os.path.join(temp_dir, 'example_config.yaml')
            save_example_config(example_path)
            
            assert os.path.exists(example_path)
            
            # Verify it can be loaded
            config = AdaptiveRAGConfig(config_file_path=example_path)
            assert config['dataset_name'] is not None


if __name__ == "__main__":
    pytest.main([__file__])
