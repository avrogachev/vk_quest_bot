from vk.keyboards import Keyboard, ButtonColor

# keyboards for teams

kb_start = Keyboard(one_time=False)
kb_start.add_text_button('Начать квест!', payload={"command": 'start'})

kb_choose = Keyboard(one_time=False)
kb_choose.add_text_button('Я капитан', payload={"command": 'kb_choose_captain'})
kb_choose.add_text_button('Я участник', payload={"command": 'kb_choose_participant'})

kb_league = Keyboard(one_time=False)
kb_league.add_text_button('Школьная', payload={"command": 'kb_school'})
kb_league.add_text_button('Молодёжная', payload={"command": 'kb_junior'})
kb_league.add_text_button('Предприятия', payload={"command": 'kb_zavod'})

kb_back_to_start = Keyboard(one_time=False)
kb_back_to_start.add_text_button('Назад', payload={"command": 'kb_back_to_start'})

kb_back_to_main = Keyboard(one_time=False)
kb_back_to_main.add_text_button('Хватит с меня этой загадки', payload={"command": 'kb_back_to_main'})

kb_main = Keyboard(one_time=False)
kb_main.add_text_button('Задания и баллы', payload={"command": 'tasks'})
# kb_main.add_text_button('Баллы команды', payload={"command": 'marks'})
kb_main.add_text_button('Помощь', payload={"command": 'help'})


# keyboards for agents
kb_agent = Keyboard(one_time=False)
kb_agent.add_text_button('Список команд', payload={"command": 'teams_agent'})  # список команд, отгадавших вашу загадку
# kb_agent.add_text_button('Баллы команд', payload={"command": 'marks_agent'})  # какие баллы и когда вы выставили
kb_agent.add_text_button('Помощь', payload={"command": 'help_agent'})  # ну тут я влетаю на помощь


kb_agent_back = Keyboard(one_time=False)
kb_agent_back.add_text_button('Не буду пока оценивать эту команду', payload={"command": 'agent_back'})
# kb_agent.add_text_button('Баллы команд', payload={"command": 'marks_agent'})  # какие баллы и когда вы выставили
# kb_agent.add_text_button('Помощь', payload={"command": 'help_agent'})  # ну тут я влетаю на помощь
# keyboards for ШТАБ

kb_admin = Keyboard(one_time=False)
kb_admin.add_text_button('Список команд', payload={"command": 'teams_admin'})
#kb_admin.add_text_button('Баллы команд', payload={"command": 'marks_admin'})
# kb_admin.add_text_button('Помощь', payload={"command": 'help'})
