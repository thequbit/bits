<%inherit file="base.mak"/>

    % if not ticket:
        <script>
            window.location.href = "/?token=${token}"
        </script>
    % endif

    % if token and user and ticket and project:

    <style>
    
        div.ticket-container {
            border-bottom: 1px solid #DDD;
            padding-bottom: 5px;
        }

        div.ticket {
            margin-top: 10px;
            border: 1px solid #DDD;
            padding: 15px;15px
        }

        textarea {
           min-height: 150px;
        }

        div.ticket-container h3 {
            margin-bottom: 0rem !important;
        }

        
 
    </style>

    <div class="row">
        <div class="medium-12 columns">
        <a href="/project?token=${token}&project_id=${project['id']}">Back to project</a>
        <br/>
        <br/>
        % if ticket:
            <div class="ticket-container">
            <h3>${ticket['title']}</h3>
            <div class="small-light-text">
                Opened by ${ticket['owner']} on ${ticket['created']}<br/><br/>
            </div>
            <div class="block-container">
                <div class="block-contents">
                    <div class="block-types">
                        <div class="block-type" style="background-color: ${ticket['type_color']};">
                            <a href="/projecttype?token=${token}&type=${ticket['type']}">${ticket['type']}</a>
                        </div>
                    </div>
                    <div class="block-contents-inner">
                        ${ticket['contents']}
                    </div>
                </div>
            </div>
            <br/> 
            
            <!-- TODO: make this pretty -->
            % for comment in comments:
                <p>${comment.contents}</p>
            % endfor

            <label>Comment</label>
            <textarea id="comment-contents" placeholder="markdown supported"></textarea>
            <a href="#" id="submit-comment" class="small radius button">Submit</a>
            <div class="right">
                <a href="#" id="submit-comment-and-close" class="small radius button">Submit and Close</a>
            </div>
        % endif
    </div>

    <script>

        $('#submit-comment').on('click', function(e) {
            console.log('sending comment')
                
            url = '/create_comment.json?token=' + localStorage.getItem("token");
            author_id = localStorage.getItem("user_id")
            project_id = ${project['id']};
            contents = $('#comment-contents').val();
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    author_id : author_id,
                    project_id : project_id,
                    contents : contents
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating ticket ...');
                    // TODO: report error
                }
            });
           
        });

        // TODO: hook up submit and close button

    </script>

    % endif
