<%inherit file="base.mak"/>

    % if project == None:
        <script>
            window.location.href = "/?token=${token}"
        </script>
    % endif

    % if user and token and project:
    <div class="row">
        <div class="medium-12 columns">
            <div class="block-container">
                <div class="block-title">
                    ${project['name']}
                </div>
                <div class="block-contents">
                    <p class="small">
                        Created: ${project['created']}<br/>
                        Owner: ${project['owner']}
                    </p>
                    <div class="inner-block-contents">
                        ${project['description']}
                    </div>
                    <!-- TODO: make project types in database, then fill this in
                    <div class="block-types">
                        <div class="block-type" style="background-color: #FF6600;">
                            <a href="/projecttype?token=${token}&type=house">house</a>
                        </div>
                    </div>
                    -->
                </div>
            </div>
            <hr/>
        </div>
    </div>

    <div class="row blocks">
        <div class="medium-4 column">
            <h4>
                <a href="/requirements?token=${token}&project_id=${project['id']}">Requirements</a>
                <small>
                    <a href="/newrequirement?token=${token}&project_id=${project['id']}">New</a>
                </small>
            </h4>
            % if not requirements or len(requirements) == 0:

                There are currently no requirements for this project. <br/><br/>

            % else:

                % for requirement in requirements:
                <div class="block-container">
                    <div class="block-title requirement-title">
                        <a href="/requirement?token=${token}&requirement_id=${requirement['id']}">${note['title']}</a>
                    </div>
                    <div class="block-contents">
                        <p class="small">
                            Created: ${requirement['created']}<br/>
                            Owner: ${requirement['owner']}
                        </p>
                        <div class="inner-block-contents">
                            ${requirement['content']}
                        </div>
                    
                        <div class="block-types">
                            <!--
                            <div class="block-type" style="background-color: #CC00FF;">main</div>
                            <div class="block-type" style="background-color: #6600FF;">v0.1</div>
                            -->
                        </div>
                    </div>
                </div>
                % endfor

            % endif
            <hr/>
        </div>

        <div class="medium-4 columns">
            <h4>
                <a href="/tickets?token=${token}&project_id=${project['id']}">Tickets</a> 
                <small>
                    <a href="/newticket?token=${token}&project_id=${project['id']}" class="small">New</a>
                </small>
            </h4>
            % if len(tickets) == 0:

                There are currently no tickets for this project.<br/><br/>  

            % else:

                % for ticket in tickets:
                <div class="block-container">
                    <div class="block-title ticket-title">
                        <a href="/ticket?token=${token}&ticket_id=${ticket['id']}&project_id=${project['id']}">${ticket['title']}</a>
                    </div>
                    <div class="block-contents">
                        <p class="small">
                            Created: ${ticket['created']}<br/>
                            Owner: ${ticket['owner']}
                        </p>
                        <div class="inner-block-contents">
                            ${ticket['contents']}
                        </div>
                        <div class="block-types">
                            <div class="block-type" style="background-color: ${ticket['type_color']};">${ticket['type']}</div>
                        </div>
                    </div>
                </div>
                <br/>
                % endfor

            % endif

            <hr/>
        </div>
 
        <div class="medium-4 column">
            <h4>
                <a href="/notes?token=${token}&project_id=${project['id']}">Notes</a>
                <small>
                    <a href="/newnote?token=${token}&project_id=${project['id']}">New</a>
                </small>
            </h4>
            % if not notes or len(notes) == 0:

                There are currently no notes for this project. <br/><br/>

            % else:

                % for note in notes:
                <div class="block-container">
                    <div class="block-title requirement-title">
                        <a href="/requirement?token=${token}&requirement_id=${requirement['id']}">${note['title']}</a>
                    </div>
                    <div class="block-contents">
                        <p class="small">
                            Created: ${note['created']}<br/>
                            Owner: ${note['owner']}
                        </p>
                        <div class="inner-block-contents">
                            ${note['content']}
                        </div>

                        <div class="block-types">
                            <!--
                            <div class="block-type" style="background-color: #CC00FF;">main</div>
                            <div class="block-type" style="background-color: #6600FF;">v0.1</div>
                            -->
                        </div>
                    </div>
                </div>
                % endfor

            % endif
            <hr/>
        </div>

    </div>
       
    % endif
