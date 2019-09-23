from vk.keyboards import Keyboard, ButtonColor

# keyboards for teams

kb_start = Keyboard(one_time=False)
kb_start.add_text_button('Начать квест!', payload={"command": 'start'})

kb_choose = Keyboard(one_time=False)
kb_choose.add_text_button('Я капитан', payload={"command": 'kb_choose_captain'})
kb_choose.add_text_button('Я участник', payload={"command": 'kb_choose_participant'})

kb_back_to_start = Keyboard(one_time=False)
kb_back_to_start.add_text_button('Назад', payload={"command": 'kb_back_to_start'})

kb_main = Keyboard(one_time=False)
kb_main.add_text_button('Задания', payload={"command": 'tasks'})
kb_main.add_text_button('Баллы команды', payload={"command": 'marks'})
kb_main.add_text_button('Помощь', payload={"command": 'help'})


# keyboards for agents
kb_agent = Keyboard(one_time=False)
kb_agent.add_text_button('Список команд', payload={"command": 'teams_agent'})  # список команд, отгадавших вашу загадку
kb_agent.add_text_button('Баллы команд', payload={"command": 'marks_agent'})  # какие баллы и когда вы выставили
kb_agent.add_text_button('Помощь', payload={"command": 'help_agent'})  # ну тут я влетаю на помощь

# keyboards for ШТАБ

kb_admin = Keyboard(one_time=False)
kb_admin.add_text_button('Список команд', payload={"command": 'teams_admin'})
kb_admin.add_text_button('Баллы команд', payload={"command": 'marks_admin'})
# kb_admin.add_text_button('Помощь', payload={"command": 'help'})
