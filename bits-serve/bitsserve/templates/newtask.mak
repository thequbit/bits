<%inherit file="base.mak"/>

    <style>
 

    </style>

    % if user and token and project:

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/project?project_id=${project['id']}">Back to Project</a>
             > New Task
            <div class="right top-links">
                <a href="/prjectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings?user_id=${user.id}">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
            <div class="container-inner box shadow">
                <h5>New Task<h5>
                <div class="small-light-text padded-bottom">
                    When creating a task, be sure to include all of the nessisary information needed 
                    to complete the task such as links, phone numbers, and/or names.  The more information
                    provided within the task, the more likely it will be completed autonomously.
                </div>
                <input id="task-title" placeholder="title" type="text"></textarea>                
                <textarea id="task-contents" placeholder="markdown supported"></textarea>
                <input id="task-assigned" placeholder="Assign task (email)" type="text">
            </div>
            <br/>
            <a href="#" id="submit-task" class="small radius button">Submit</a>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tasks
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
                            <div class="short-line-height extra-small-light-text">
                                opened by ${task['owner']} on ${task['created']}
                            </div>
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
            var assigned = $('#task-assigned').val();

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    project_id : project_id,
                    title : title,
                    contents : contents,
                    assigned : assigned,
                    //due : due,
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
                    console.log(data);
                    // TODO: report error
                }
            });

        });

        // TODO: hook up submit and close button

    </script>

    % endif
