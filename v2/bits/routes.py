def includeme(config):

	# set cache age to 1 second for development - we should be serving up 
	# static assets with nginx anyway ...
    config.add_static_view('static', 'static', cache_max_age=1)
    
    # pages
    config.add_route('/', '/')
    config.add_route('/login', '/login')
    config.add_route('/logout', '/logout')

    # users
    config.add_route('/api/v1/users/_login', '/api/v1/users/_login')
    config.add_route('/api/v1/users/_logout', '/api/v1/users/_logout')
    config.add_route('/api/v1/users/_exists', '/api/v1/users/_exists')
    config.add_route('/api/v1/users', '/api/v1/users')
    config.add_route('/api/v1/users/{id}', '/api/v1/users/{id}')
    config.add_route('/api/v1/users/{id}/_change_password', '/api/v1/users/{id}/_change_password')
    config.add_route('/api/v1/users/{id}/_status', '/api/v1/users/{id}/_status')

    # note_kudos
    config.add_route('/api/v1/note_kudos', '/api/v1/note_kudos')
    config.add_route('/api/v1/note_kudos/{id}', '/api/v1/note_kudos/{id}')

    # notes
    config.add_route('/api/v1/notes', '/api/v1/notes')
    config.add_route('/api/v1/notes/{id}', '/api/v1/notes/{id}')    

    # organizations
    config.add_route('/api/v1/organizations', '/api/v1/organizations')
    config.add_route('/api/v1/organizations/{id}', '/api/v1/organizations/{id}')    

    # tasks
    config.add_route('/api/v1/tasks', '/api/v1/tasks')
    config.add_route('/api/v1/tasks/{id}', '/api/v1/tasks/{id}')    


    # milestones
    config.add_route('/api/v1/milestones', '/api/v1/milestones')
    config.add_route('/api/v1/milestones/{id}', '/api/v1/milestones/{id}')

    # projects
    config.add_route('/api/v1/projects', '/api/v1/projects')
    config.add_route('/api/v1/projects/{id}', '/api/v1/projects/{id}')

    # settings
    config.add_route('/api/v1/settings', '/api/v1/settings')
    config.add_route('/api/v1/settings/{id}', '/api/v1/settings/{id}')
