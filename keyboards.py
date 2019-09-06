from vk.keyboards import Keyboard, ButtonColor

kb_cpt = Keyboard(one_time=False)
kb_cpt.add_text_button('Hi', payload={"command": 'hello'})
kb_cpt.add_text_button("Bye:(", payload={"command": 'bye'}, color=ButtonColor.SECONDARY)

keyboard_start = Keyboard(one_time=True)
keyboard_start.add_text_button('Начинаем квест!', payload={"command": 'start'})