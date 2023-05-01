from imap_tools import MailBox, A, H
import os
import webbrowser


def clear():
    os_name = os.name
    if os_name == "nt":
        os.system("cls")
    elif os_name == "posix":
        os.system("clear")


def get_accounts():
    with open('creditials.txt') as file:
        accounts = file.read().split('\n')
        if not accounts[-1]:
            accounts = accounts[:-1]
        for i in range(len(accounts)):
            accounts[i] = accounts[i].split(':')
        file.close()
        return accounts


def actions(account_login, account_password):
    clear()
    try:
        mailbox = MailBox('imap.rambler.ru').login(account_login, account_password)
    except:
        print(f'Не удалось войти в аккаунт {account_login}\n\nEnter, чтобы вернуться')
        input()
        return

    messages = []
    for msg in mailbox.fetch():
        messages.append((msg.uid, msg.subject))

    messages_text = '\n'.join(f'[{i + 1}] {messages[i][1]}' for i in range(len(messages)))

    while 1:
        clear()
        print(f'[{account_login}]\n\n{messages_text}\n[0] Вернуться\n')
        choice = input('Выбор: ')

        try:
            int(choice)
        except ValueError:
            continue

        if choice == '0':
            return

        if not (0 <= int(choice) - 1 < len(messages)):
            continue

        clear()
        try:
            message = list(mailbox.fetch(A(uid=messages[int(choice) - 1][0])))[0]
        except:
            print('Не удалось получить данные сообщения\n')
            input('Enter, чтобы вернуться...')
        else:
            try:
                with open('message.html', 'w', encoding='utf-8') as file:
                    file.write(message.html)
                    file.close()
                webbrowser.open(f'file:///{os.getcwd()}/message.html')
            except:
                print(message.text)
                input('\nEnter, чтобы вернуться...')


def main():
    accounts = get_accounts()
    while 1:
        clear()
        accounts_text = '\n'.join(f'[{i + 1}] {accounts[i][0]}' for i in range(len(accounts)))
        print(f'[Выбор аккаунта]\n\n{accounts_text}\n[0] Выйти\n')
        choice = input('Выбор: ')

        try:
            int(choice)
        except ValueError:
            continue

        if choice == '0':
            return

        if not (0 <= int(choice) - 1 < len(accounts)):
            continue

        actions(*accounts[int(choice) - 1])


if __name__ == '__main__':
    main()
