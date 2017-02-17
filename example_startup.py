from dragonbot import DragonBot

def main(test_mode = True):

    """Example DragonBot configuration file."""

    bot = DragonBot()

    bot.setup("localhost", port = 6667,
              password = "hunter2",
              nick = "Toothless")

    bot.admins(["StoickTheVast"])
    bot.devs(["Hiccup", "Astrid"])

    bot.skills("skills", "skills.db")

    if not test_mode:

        bot.start_client()

    else:

        bot.start_shell()


if __name__ == "__main__":

    main(test_mode = False)
