<%inherit file="base.mak"/>

    <style>
 
        div.new-project-container {
            padding: 10px;
        }

    </style>

    % if user:

    <div class="row">
        <div class="large-12 columns">
            <a href="/">Back to Project</a>
        </div>
    </div> 

    <div class="row">
        <div class="medium-8 columns">
            <div class="new-project-container box shadow">
                <h5>New Project<h5>
                <input type="text" id="project-name" placeholder="Project Name"></text>
                <div class="right"><small>Markdown Supported</small></div>
                <textarea id="project-description" placeholder="Project Description"></textarea>
            </div>
            <br/>
            <a href="#" id="submit-project" class="small radius button">Submit</a>
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
        </div>
    </div>

    <script>

        $('#submit-project').on('click', function(e) {

            console.log('sending comment')

            var token = document.cookie.split('=')[1];
            var url = '/create_project.json';
            var name = $('#project-name').val();
            var description = $('#project-description').val();

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

        });

        // TODO: hook up submit and close button

    </script>

    % endif
