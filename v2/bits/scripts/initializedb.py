import os
import sys
import transaction
import hashlib

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import (
    Organizations,
    Users,
    #ProjectStates,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    dbsession = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:

        #
        # system user - can do it all.
        #

        _system_organization = Organizations.add(
            dbsession=dbsession,
            name="System Organization",
            description="",
        )

        _system_user = Users.create_new_user(
            dbsession=dbsession,
            organization_id=_system_organization.id,
            first='SYSTEM',
            last='USER',
            phone='000-000-0000',
            email='system',
            password=hashlib.sha256('password'.encode('utf-8')).hexdigest(),
            user_type='system',
            enabled=1,
            deleted=False,
        )