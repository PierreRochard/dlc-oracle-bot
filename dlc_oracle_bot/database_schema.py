from dlc_oracle_bot.models import Sources


def main():
    from dlc_oracle_bot.database.migrations import create_or_update_database
    from dlc_oracle_bot.database.session_scope import session_scope
    from dlc_oracle_bot.logging_utility import log

    create_or_update_database(echo=True)
    with session_scope(echo=True) as session:
        log.debug('session_scope', session=session)
        sources = session.query(Sources).all()
        print(sources)


if __name__ == '__main__':

    try:
        main()
    except ModuleNotFoundError as e:
        print(e)
        from dlc_oracle_bot.install_requirements import install_requirements

        install_requirements()
