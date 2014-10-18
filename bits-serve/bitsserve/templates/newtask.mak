<%inherit file="base.mak"/>

    <style>
 

    </style>

    % if user and token and project:

    <div class="row">
        <div class="large-12 columns">
            <a href="/">Back to Project</a>
        </div>
    </div> 

    <div class="row">
        <div class="medium-8 columns">
            <div class="container-inner box shadow">
                <h5>New Task<h5>
                <textarea id="task-contents" placeholder="markdown supported"></textarea>
            </div>
            <br/>
            <a href="#" id="submit-task" class="small radius button">Submit</a>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tickets
                    <!--<div class="right">
                        <a href="/newtask?project_id=${project['id']}">New</a>
                    </div>-->
                </div>
                % if not tasks:
                    <div class="indent">
                        <div class="small-light-text">No tasks for this project.</div>
                    </div>
                % else:
                    % for task in tasks:
                        <div class="box-inner-container">
                            <a href="/task?task_id=${task['id']}">${task['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${task['owner']} on ${task['created']}</div>
                        </div>
                    % endfor
                % endif
            </div> 
        </div>
    </div>

    <script>

        $('#submit-task').on('click', function(e) {

            console.log('sending comment')

            var token = document.cookie.split('=')[1];
            var url = '/create_task.json';
            var project_id = ${project['id']}
            var title = $('#task-title').val();
            var contents = $('#task-contents').val();

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    project_id : project_id,
                    title : title,
                    contents : contents
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/task?task_id=" + data.task_id;
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating task ...');
                    // TODO: report error
                }
            });

        });

        // TODO: hook up submit and close button

    </script>

    % endif
