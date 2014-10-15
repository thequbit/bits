<%inherit file="base.mak"/>

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

        div.comment-container {
            
        }

        div.comment-container-inner {
            padding: 10px;
            
        }
        
 
    </style>

    <div class="row">
        <div class="large-12 columns">
            <a href="/">Back to Project</a>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
        % if ticket:
            <div class="ticket-container">
                <h3>${ticket['title']}</h3>
                <div class="small-light-text">
                    Opened by ${ticket['owner']} on ${ticket['created']}
                </div>
                <div class="block-type" style="background-color: ${ticket['type_color']};">
                    <a href="/projecttype?token=${token}&type=${ticket['type']}">${ticket['type']}</a>
                </div>
                <div class="indent indent-right">
                    <div class="box shadow">
                        <div class="comment-container-inner">
                            ${ticket['contents'] | n}
                        </div>
                    </div>
                </div>
                <br/>           
 
                <h5>Comments</h5>            

                % for comment in comments:
                    <div class="comment-containeri box shadow">
                        <div class="small-light-text">
                            On ${comment['created']} <a href="/user?user_id=${comment['owner_id']}">${comment['owner']}</a> wrote:
                        </div>
                        <div class="comment-container-inner">
                            ${comment['contents'] | n}
                        </div>
                    </div>
                % endfor
                <br/>

                <div>
                    <label>Add Comment</label>
                    <textarea id="comment-contents" placeholder="markdown supported"></textarea>
                    <a href="#" id="submit-comment" class="small radius button">Submit</a>
                    <div class="right">
                        <a href="#" id="submit-comment-and-close" class="small radius button">Submit and Close</a>
                    </div>
                </div>
            </div>
        % endif
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tickets
                    <!--<div class="right">
                        <a href="/newticket?project_id=${project['id']}">New</a>
                    </div>-->
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for existing_ticket in tickets:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${existing_ticket['id']}">${existing_ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${existing_ticket['owner']} on ${existing_ticket['created']}</div>
                        </div>
                    % endfor
                % endif
            </div>
        </div> 
    </div>

    <script>

        $('#submit-comment').on('click', function(e) {
            
            console.log('sending comment')
            
            var token = document.cookie.split('=')[1]; 
            var url = '/create_comment.json?token=' + token;
            var ticket_id = ${ticket['id']}
            //var author_id = localStorage.getItem("user_id")
            //var project_id = ${project['id']};
            var contents = $('#comment-contents').val();
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                    //author_id : author_id,
                    //project_id : project_id,
                    contents : contents
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
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
