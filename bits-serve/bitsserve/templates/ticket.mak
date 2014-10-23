<%inherit file="base.mak"/>

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

        div.container-inner {
            padding: 10px;            
        }
        
        div.container-inner p {
            margin-bottom: 0px !important;
        }
        
        h4.closed-label {
            margin-left: 20px;
            color: red;
            font-weight: bold;
        }
        
 
    </style>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > 
            <a href="/tickets?project_id=${project['id']}">Tickets</a>
             > Ticket
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
        % if ticket:
            <div class="ticket-container">
                <div style="display: inline-flex;">
                <h4>Ticket #${ticket['number']} : ${ticket['title']}</h4>
                % if ticket['closed'] == True:
                    <h4 class="closed-label">[CLOSED]</h4>
                % endif
                </div>
                
                <div class="small-light-text">
                    Opened by ${ticket['owner']} on ${ticket['created']}
                </div>
               
                <div class="indent indent-right">
                    <div class="box shadow">
                        <div class="container-inner">
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
                        <div class="container-inner">
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

        function submit_comment(callback) {
        
            //var token = document.cookie.split('=')[1]; 
            var url = '/create_ticket_comment.json';
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
                        callback();
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
        }

        function close_ticket() {
            
            //var token = document.cookie.split('=')[1]; 
            var url = '/close_ticket.json';
            var ticket_id = ${ticket['id']}
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while closing ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
            
        }

        $('#submit-comment').on('click', function(e) {
            submit_comment();
        });
        
        $('#submit-comment-and-close').on('click', function(e) {
            close_ticket();
        });

    </script>
