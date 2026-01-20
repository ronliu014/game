"""
Unit tests for GameState and StateMachine

Tests game state management and state transitions.

Author: Circuit Repair Game Team
Date: 2026-01-20
"""

import unittest
from unittest.mock import Mock

from src.core.game_state.game_state import GameState
from src.core.game_state.state_machine import StateMachine


class TestGameState(unittest.TestCase):
    """Test GameState enum"""

    def test_all_states_defined(self):
        """测试所有状态都已定义"""
        expected_states = {'INIT', 'LOADING', 'PLAYING', 'VICTORY', 'PAUSED', 'EXITING'}
        actual_states = {state.name for state in GameState}

        self.assertEqual(actual_states, expected_states)

    def test_state_values(self):
        """测试状态值"""
        self.assertEqual(GameState.INIT.value, "init")
        self.assertEqual(GameState.LOADING.value, "loading")
        self.assertEqual(GameState.PLAYING.value, "playing")
        self.assertEqual(GameState.VICTORY.value, "victory")
        self.assertEqual(GameState.PAUSED.value, "paused")
        self.assertEqual(GameState.EXITING.value, "exiting")

    def test_state_str(self):
        """测试状态字符串表示"""
        self.assertEqual(str(GameState.INIT), "init")
        self.assertEqual(str(GameState.PLAYING), "playing")

    def test_state_repr(self):
        """测试状态详细表示"""
        self.assertEqual(repr(GameState.INIT), "GameState.INIT")
        self.assertEqual(repr(GameState.PLAYING), "GameState.PLAYING")


class TestStateMachineInitialization(unittest.TestCase):
    """Test StateMachine initialization"""

    def test_init_state(self):
        """测试初始状态"""
        machine = StateMachine()

        self.assertEqual(machine.get_current_state(), GameState.INIT)
        self.assertIsNone(machine.get_previous_state())

    def test_is_in_init_state(self):
        """测试是否在初始状态"""
        machine = StateMachine()

        self.assertTrue(machine.is_in_state(GameState.INIT))
        self.assertFalse(machine.is_in_state(GameState.PLAYING))


class TestStateMachineValidTransitions(unittest.TestCase):
    """Test valid state transitions"""

    def setUp(self):
        self.machine = StateMachine()

    def test_init_to_loading(self):
        """测试从INIT到LOADING的转换"""
        success = self.machine.transition_to(GameState.LOADING)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.LOADING)
        self.assertEqual(self.machine.get_previous_state(), GameState.INIT)

    def test_init_to_exiting(self):
        """测试从INIT到EXITING的转换"""
        success = self.machine.transition_to(GameState.EXITING)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.EXITING)

    def test_loading_to_playing(self):
        """测试从LOADING到PLAYING的转换"""
        self.machine.transition_to(GameState.LOADING)
        success = self.machine.transition_to(GameState.PLAYING)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.PLAYING)

    def test_playing_to_victory(self):
        """测试从PLAYING到VICTORY的转换"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        success = self.machine.transition_to(GameState.VICTORY)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.VICTORY)

    def test_playing_to_paused(self):
        """测试从PLAYING到PAUSED的转换"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        success = self.machine.transition_to(GameState.PAUSED)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.PAUSED)

    def test_paused_to_playing(self):
        """测试从PAUSED到PLAYING的转换"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.PAUSED)
        success = self.machine.transition_to(GameState.PLAYING)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.PLAYING)

    def test_victory_to_loading(self):
        """测试从VICTORY到LOADING的转换（下一关）"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.VICTORY)
        success = self.machine.transition_to(GameState.LOADING)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.LOADING)

    def test_victory_to_init(self):
        """测试从VICTORY到INIT的转换（返回主菜单）"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.VICTORY)
        success = self.machine.transition_to(GameState.INIT)

        self.assertTrue(success)
        self.assertEqual(self.machine.get_current_state(), GameState.INIT)


class TestStateMachineInvalidTransitions(unittest.TestCase):
    """Test invalid state transitions"""

    def setUp(self):
        self.machine = StateMachine()

    def test_init_to_playing(self):
        """测试从INIT直接到PLAYING（无效）"""
        success = self.machine.transition_to(GameState.PLAYING)

        self.assertFalse(success)
        self.assertEqual(self.machine.get_current_state(), GameState.INIT)

    def test_init_to_victory(self):
        """测试从INIT直接到VICTORY（无效）"""
        success = self.machine.transition_to(GameState.VICTORY)

        self.assertFalse(success)
        self.assertEqual(self.machine.get_current_state(), GameState.INIT)

    def test_loading_to_victory(self):
        """测试从LOADING直接到VICTORY（无效）"""
        self.machine.transition_to(GameState.LOADING)
        success = self.machine.transition_to(GameState.VICTORY)

        self.assertFalse(success)
        self.assertEqual(self.machine.get_current_state(), GameState.LOADING)

    def test_exiting_to_any_state(self):
        """测试从EXITING到任何状态（无效，终止状态）"""
        self.machine.transition_to(GameState.EXITING)

        # Try all possible transitions from EXITING
        self.assertFalse(self.machine.transition_to(GameState.INIT))
        self.assertFalse(self.machine.transition_to(GameState.LOADING))
        self.assertFalse(self.machine.transition_to(GameState.PLAYING))
        self.assertFalse(self.machine.transition_to(GameState.VICTORY))
        self.assertFalse(self.machine.transition_to(GameState.PAUSED))

        self.assertEqual(self.machine.get_current_state(), GameState.EXITING)

    def test_invalid_state_type(self):
        """测试无效的状态类型"""
        success = self.machine.transition_to("invalid")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_current_state(), GameState.INIT)


class TestStateMachineCanTransition(unittest.TestCase):
    """Test can_transition_to method"""

    def setUp(self):
        self.machine = StateMachine()

    def test_can_transition_from_init(self):
        """测试从INIT可以转换的状态"""
        self.assertTrue(self.machine.can_transition_to(GameState.LOADING))
        self.assertTrue(self.machine.can_transition_to(GameState.EXITING))
        self.assertFalse(self.machine.can_transition_to(GameState.PLAYING))
        self.assertFalse(self.machine.can_transition_to(GameState.VICTORY))
        self.assertFalse(self.machine.can_transition_to(GameState.PAUSED))

    def test_can_transition_from_playing(self):
        """测试从PLAYING可以转换的状态"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        self.assertTrue(self.machine.can_transition_to(GameState.VICTORY))
        self.assertTrue(self.machine.can_transition_to(GameState.PAUSED))
        self.assertTrue(self.machine.can_transition_to(GameState.LOADING))
        self.assertTrue(self.machine.can_transition_to(GameState.EXITING))
        self.assertFalse(self.machine.can_transition_to(GameState.INIT))

    def test_can_transition_from_exiting(self):
        """测试从EXITING不能转换到任何状态"""
        self.machine.transition_to(GameState.EXITING)

        self.assertFalse(self.machine.can_transition_to(GameState.INIT))
        self.assertFalse(self.machine.can_transition_to(GameState.LOADING))
        self.assertFalse(self.machine.can_transition_to(GameState.PLAYING))
        self.assertFalse(self.machine.can_transition_to(GameState.VICTORY))
        self.assertFalse(self.machine.can_transition_to(GameState.PAUSED))


class TestStateMachineGetValidTransitions(unittest.TestCase):
    """Test get_valid_transitions method"""

    def setUp(self):
        self.machine = StateMachine()

    def test_get_valid_transitions_from_init(self):
        """测试获取INIT状态的有效转换"""
        valid = self.machine.get_valid_transitions()

        self.assertEqual(len(valid), 2)
        self.assertIn(GameState.LOADING, valid)
        self.assertIn(GameState.EXITING, valid)

    def test_get_valid_transitions_from_playing(self):
        """测试获取PLAYING状态的有效转换"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        valid = self.machine.get_valid_transitions()

        self.assertEqual(len(valid), 4)
        self.assertIn(GameState.VICTORY, valid)
        self.assertIn(GameState.PAUSED, valid)
        self.assertIn(GameState.LOADING, valid)
        self.assertIn(GameState.EXITING, valid)

    def test_get_valid_transitions_from_exiting(self):
        """测试获取EXITING状态的有效转换（空集）"""
        self.machine.transition_to(GameState.EXITING)

        valid = self.machine.get_valid_transitions()

        self.assertEqual(len(valid), 0)


class TestStateMachineCallbacks(unittest.TestCase):
    """Test state callback functionality"""

    def setUp(self):
        self.machine = StateMachine()
        self.callback_called = False
        self.callback_state = None

    def _test_callback(self):
        """测试回调函数"""
        self.callback_called = True

    def test_register_callback(self):
        """测试注册回调"""
        self.machine.register_callback(GameState.PLAYING, self._test_callback)

        self.machine.transition_to(GameState.LOADING)
        self.assertFalse(self.callback_called)

        self.machine.transition_to(GameState.PLAYING)
        self.assertTrue(self.callback_called)

    def test_callback_not_called_on_invalid_transition(self):
        """测试无效转换不调用回调"""
        self.machine.register_callback(GameState.PLAYING, self._test_callback)

        # Try invalid transition
        self.machine.transition_to(GameState.PLAYING)

        self.assertFalse(self.callback_called)

    def test_unregister_callback(self):
        """测试取消注册回调"""
        self.machine.register_callback(GameState.PLAYING, self._test_callback)
        self.machine.unregister_callback(GameState.PLAYING)

        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        self.assertFalse(self.callback_called)

    def test_register_invalid_callback(self):
        """测试注册无效回调"""
        # Should not raise exception
        self.machine.register_callback(GameState.PLAYING, "not_callable")

        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        # Should still transition successfully
        self.assertEqual(self.machine.get_current_state(), GameState.PLAYING)

    def test_callback_exception_handling(self):
        """测试回调异常处理"""
        def failing_callback():
            raise ValueError("Test exception")

        self.machine.register_callback(GameState.PLAYING, failing_callback)

        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        # Should still transition successfully despite callback error
        self.assertEqual(self.machine.get_current_state(), GameState.PLAYING)

    def test_multiple_callbacks(self):
        """测试多个状态的回调"""
        loading_called = False
        playing_called = False

        def loading_callback():
            nonlocal loading_called
            loading_called = True

        def playing_callback():
            nonlocal playing_called
            playing_called = True

        self.machine.register_callback(GameState.LOADING, loading_callback)
        self.machine.register_callback(GameState.PLAYING, playing_callback)

        self.machine.transition_to(GameState.LOADING)
        self.assertTrue(loading_called)
        self.assertFalse(playing_called)

        self.machine.transition_to(GameState.PLAYING)
        self.assertTrue(playing_called)


class TestStateMachineReset(unittest.TestCase):
    """Test state machine reset functionality"""

    def setUp(self):
        self.machine = StateMachine()

    def test_reset_from_playing(self):
        """测试从PLAYING重置"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        self.machine.reset()

        self.assertEqual(self.machine.get_current_state(), GameState.INIT)
        self.assertEqual(self.machine.get_previous_state(), GameState.PLAYING)

    def test_reset_from_init(self):
        """测试从INIT重置"""
        self.machine.reset()

        self.assertEqual(self.machine.get_current_state(), GameState.INIT)
        self.assertEqual(self.machine.get_previous_state(), GameState.INIT)

    def test_reset_clears_previous_state(self):
        """测试重置后可以正常转换"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.reset()

        # Should be able to transition from INIT again
        success = self.machine.transition_to(GameState.LOADING)
        self.assertTrue(success)


class TestStateMachineComplexScenarios(unittest.TestCase):
    """Test complex state transition scenarios"""

    def setUp(self):
        self.machine = StateMachine()

    def test_complete_game_flow(self):
        """测试完整游戏流程"""
        # Start game
        self.assertTrue(self.machine.transition_to(GameState.LOADING))
        self.assertTrue(self.machine.transition_to(GameState.PLAYING))

        # Pause and resume
        self.assertTrue(self.machine.transition_to(GameState.PAUSED))
        self.assertTrue(self.machine.transition_to(GameState.PLAYING))

        # Win level
        self.assertTrue(self.machine.transition_to(GameState.VICTORY))

        # Load next level
        self.assertTrue(self.machine.transition_to(GameState.LOADING))
        self.assertTrue(self.machine.transition_to(GameState.PLAYING))

        # Exit game
        self.assertTrue(self.machine.transition_to(GameState.EXITING))

    def test_restart_level_flow(self):
        """测试重新开始关卡流程"""
        # Start level
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)

        # Restart level (go back to loading)
        self.assertTrue(self.machine.transition_to(GameState.LOADING))
        self.assertTrue(self.machine.transition_to(GameState.PLAYING))

    def test_return_to_menu_from_victory(self):
        """测试从胜利返回主菜单"""
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.VICTORY)

        # Return to menu
        self.assertTrue(self.machine.transition_to(GameState.INIT))

    def test_exit_from_any_state(self):
        """测试从任何状态退出（除了EXITING）"""
        # From INIT
        self.assertTrue(self.machine.transition_to(GameState.EXITING))

        # Reset and try from LOADING
        self.machine.reset()
        self.machine.transition_to(GameState.LOADING)
        self.assertTrue(self.machine.transition_to(GameState.EXITING))

        # Reset and try from PLAYING
        self.machine.reset()
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.assertTrue(self.machine.transition_to(GameState.EXITING))

        # Reset and try from PAUSED
        self.machine.reset()
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.PAUSED)
        self.assertTrue(self.machine.transition_to(GameState.EXITING))

        # Reset and try from VICTORY
        self.machine.reset()
        self.machine.transition_to(GameState.LOADING)
        self.machine.transition_to(GameState.PLAYING)
        self.machine.transition_to(GameState.VICTORY)
        self.assertTrue(self.machine.transition_to(GameState.EXITING))


if __name__ == '__main__':
    unittest.main()
