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

        div.ticket textarea {
           min-height: 150px;
        }

        div.indent {
            padding-left: 25px;
        }
 
    </style>

    <div class="ticket">
        % if ticket:
            <h4>${ticket[16]}</h4>
            <div class="indent"><small>Opened by: ${ticket[4]} ${ticket[5]} </small><br/></div>
            <div class="indent"><small>Opened on: ${ticket[3]}</small><br/></div>
            <div class="ticket">
                <p>${ticket[17]}</p>
            </div>

            % for comment in comments:
                <p>${comment.contents}</p>
            % endfor

            <label>Comment</label>
            <textarea id="comment-contents" placeholder="markdown supported"></textarea>
            <a href="#" onclick="submit_comment();" id="submit-comment" class="small radius button">Submit</a>
        % endif
    </div>

    <script>

        console.log('log test');

        
        $('#submit-comment').on('click', function(e) {
            console.log('sending comment')
                
            url = '/create_comment.json?token=' + localStorage.getItem("token");
            author_id = localStorage.getItem("user_id")
            project_id = ${project_id};
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

    </script>
