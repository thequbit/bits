<%inherit file="base.mak"/>

    <style>
 
        div.new-project-container {
            padding: 10px;
        }

    </style>


    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/projects">Projects</a>
             >
            New Project
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
            <div class="new-project-container box shadow">
                <div class="row">
                    <div class="medium-12 columns">
                        <h5>New Project
                        <div class="right small-light-text markdown-boxi markdown-text">Markdown Supported</div>
                        </h5>
                     </div>
                </div>
                <input type="text" id="project-name" placeholder="Project Name"></text>
                <textarea id="project-description" placeholder="Project Description"></textarea>
            </div>
            <div id="error-message-wrapper" class="box shadow error-box" style="display: none;">
                <div id="error-message" class="container-inner box-small-text"></div>
            </div>
            <br/>
            <a href="#" id="submit-project" class="small radius button">Create Project</a>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Projects
                </div>
                % if not projects:
                    <div class="indent">
                        <div class="small-light-text">There are no projects yet.</div>
                    </div>
                % else:
                    % for project in projects:
                        <div class="box-inner-container">
                            <a href="/project?project_id=${project['id']}">${project['name']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${project['owner']} on ${project['created']}</div>
                        </div>
                    % endfor
                % endif
            </div>
            <hr/> 
        </div>
    </div>

    <script>

        $('#submit-project').on('click', function(e) {

            show_loading();

            var token = document.cookie.split('=')[1];
            var url = '/create_project.json';
            var name = $('#project-name').val();
            var description = $('#project-description').val();

            if ( name == '' ) {
                console.log('error: name can not be blank');
                display_error('The project must at least have a name');
            }
            else {
 
                $.ajax({
                    dataType: 'json',
                    type: 'POST',
                    data: {
                        name : name,
                        description : description
                    },
                    url: url,
                    success: function(data) {
                        if( data.success == true ) {
                            console.log('SUCCESS!');
                            window.location.href="/project?project_id=" + data.project_id;
                        }
                    },
                    error: function(data) {
                        console.log('an error happened while creating project ...');
                        // TODO: report error
                    }
                });
            }

        });

        function display_error(error_text) {
            console.log('displaying error');
            $('#error-message').html('Error: ' + error_text);
            $('#error-message-wrapper').show();
        }

    </script>