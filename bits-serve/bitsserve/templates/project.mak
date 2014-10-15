<%inherit file="base.mak"/>

    <style>

        div.inner-container {
            margin-bottom: 10px;
        }

        div.inner-container .extra-small-light-text {
            line-height: 75% !important;
        }

    </style>

    % if user and token and project:

    <div class="row">
        <div class="large-12 columns">
            <a href="/">Home</a>
        </div>
    </div>

    <div class="row">
        <div class="medium-4 columns">
            <h5>${project['name']} <small>${project['owner']}</small></h5>
        </div>
        <hr/>
    </div>
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title"> 
                    Requirements
                    <div class="right">
                        <a href="/newrequirment?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not requirements:
                    <div class="indent">
                        <div class="small-light-text">No requirements for this project.</div>
                    </div>
                % else:
                    % for requirement in requirements:
                        <div class="box-inner-container">
                            <a href="/requirement?requirement_id=${requirement['id']}">${requirement['name']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${requirement['owner']} on ${requirement['created']}</div>
                        </div>
                    % endfor
                % endif 
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Tickets
                    <div class="right">
                        <a href="/newticket?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for ticket in tickets:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${ticket['owner']} on ${ticket['created']}</div>
                        </div>
                    % endfor
                % endif
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Notes
                    <div class="right">
                        <a href="/newnote?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not notes:
                    <div class="indent">
                        <div class="small-light-text">No notess for this project.</div>
                    </div>
                % else:
                    % for note in notes:
                        <div class="box-inner-container">
                            <div class="indent">
                                <a href="/note?ticket_id=${note['id']}">${note['title']}</a>
                                <div class="short-line-height extra-small-light-text"> opened by ${note['owner']} on ${note['created']}</div>
                            </div>
                        </div>
                    % endfor
                % endif
            </div>
        </div>
    </div>

    % endif
