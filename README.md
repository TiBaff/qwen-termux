# qwen-termux
RU:
Привет! Я недавно копался в теме ИИ, чтобы получить у нему доступ абсолютно без интернета. И я нашел! В этом репозитории лежит все что нужно для установки Qwen (в обычном и думающем режиме) прямо на телефон.
### Плюсы такого ИИ:
1. Доступен без интернета.
2. Можно задавать свой системный промпт.
3. Запоминает диалог с тобой, записывая его в отдельный файл.
### Минусы такого ИИ:
1. Работает достаточно медленно (с 12 гб оперативной памяти в обычном режиме ~12 секунд на первое сообщение, ~4 минуты в думающем режиме), но все зависит от телефона и количества на нем оперативной памяти.
2. Весит очень много для своих способностей. Для полноценной работы ИИ вам нужно минимум 10 гб свободного места. Занимаемое место может увеличиваться за счет записи диалога, но память можно очистить (команда /clear).
3. Общается только текстом (можно добавить генерацию фото, но это будет весить минимум 20 гб, требовать от 20-30 гб оперативки и ждать надо будет от получаса).

### Для установки:
1. Установите qwen-termux: `curl -fsSL https://raw.githubusercontent.com/TiBaff/qwen-termux/refs/heads/main/install.sh | bash`
2. Запустите ollama: `ollama serve > /dev/null 2>&1 &`
3. После запустите ИИ: `python ~/ai/ai.py`
### ПРИМЕЧАНИЕ:
Данный проект может не работать, так как он находится в ранней стадии разработки.

Статус проекта: В разработке.
***
ENG:
Hi! I recently dug into the topic of AI to get access to it completely without the internet. And I found it! This repository contains everything you need to install Qwen (in normal and thinking mode) directly on your phone.
### Pros of such AI:
1. Available without the internet.
2. You can set your own system prompt.
3. Remembers the dialogue with you by recording it in a separate file.
### Cons of such AI:
1. Works quite slowly (with 12 GB of RAM in normal mode ~12 seconds for the first message, ~4 minutes in thinking mode), but it all depends on the phone and the amount of RAM on it.
2. Weighs a lot for its capabilities. For the AI to function fully, you need at least 10 GB of free space. The occupied space may increase due to dialogue recording, but the memory can be cleared (command /clear).
3. Communicates only via text (you can add photo generation, but it will weigh at least 20 GB, require 20-30 GB of RAM, and you will have to wait for half an hour or more).

### To install:
 1. Install qwen-termux: `curl -fsSL https://raw.githubusercontent.com/TiBaff/qwen-termux/refs/heads/main/install.sh | bash`
 2. Start ollama: `ollama serve > /dev/null 2>&1 &`
 3. Then launch the AI: `python ~/ai/ai.py`
### NOTE:
This project may not work as it is in an early stage of development.
Project status: In development.
