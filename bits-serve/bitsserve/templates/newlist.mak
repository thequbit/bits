<%inherit file="base.mak"/>

    <style>

        h6 {
            margin-left: 20px;
        }

        #list-items input {
            margin-left: 20px !important;
            width: 75% !important;
        }

        #new-item {
            margin-left: 20px !important;
        }

 
    </style>

    % if user and token and project:

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/project?project_id=${project['id']}">Back to Project</a>
             > New List
            <div class="right top-links">
                <a href="/prjectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings?user_id=${user.id}">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
            <div class="container-inner box shadow">
                <h5>New List<h5>
                <input type="text" id="list-name" placeholder="liast name"></text>
                <!--<textarea id="list-contents" placeholder="markdown supported"></textarea>-->
                <h6 style="margin-left: 20px;">Items</h6>
                <div id="list-items">
                </div>
                <a href="#" id="new-item"><div class="small-text">Add Item</div></a>
            </div>
            <br/>
            <a href="#" id="submit-liast" class="small radius button">Submit</a>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Lists
                    <!--<div class="right">
                        <a href="/newlist?project_id=${project['id']}">New</a>
                    </div>-->
                </div>
                % if not lists:
                    <div class="indent">
                        <div class="small-light-text">No lists for this project.</div>
                    </div>
                % else:
                    % for list in lists:
                        <div class="box-inner-container">
                            <a href="/list?list_id=${list['id']}">${list['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${list['owner']} on ${list['created']}</div>
                        </div>
                    % endfor
                % endif
            </div> 
        </div>
    </div>

    <script>

        //
        // via: http://stackoverflow.com/a/1349426
        //
        function makeid()
        {
            var text = "";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

            for( var i=0; i < 10; i++ )
                text += possible.charAt(Math.floor(Math.random() * possible.length));

            return text;
        }

        $('#new-item').on('click', function(e) {
            var id = makeid();
            html = $('#list-items').html();
            new_html = '<input type="text" + id="' + id + '">';
            new_html += '<a href="#" id="' + id +'">remove</a>';
            $('#list-items').html(new_html + html);
            $('#'+id).on('click', function(e) {
                // TODO, remove item
            }
        })

        $('#submit-list').on('click', function(e) {

            console.log('sending comment')

            var token = document.cookie.split('=')[1];
            var url = '/create_list.json';
            var project_id = ${project['id']}
            var title = $('#list-title').val();
            var contents = $('#list-contents').val();

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
                        window.location.href="/list?list_id=" + data.list_id;
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating list ...');
                    // TODO: report error
                }
            });

        });

        // TODO: hook up submit and close button

    </script>

    % endif
