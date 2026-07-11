- name: Run bot
  env:
    TOKEN: ${{ secrets.TOKEN }}
  run: python bot.py
