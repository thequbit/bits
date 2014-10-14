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
        <div class="medium-4 columns">
            <h5>${project['name']} <small>${project['owner']}</small></h5>
        </div>
        <hr/>
    </div>
    <div class="row">
        <div class="medium-4 columns">
            <div class="box">
                <div class="box-title"> 
                    Requirements
                    <div class="right">
                        <a href="/newrequirment">New</a>
                    </div>
                </div>
                % if not requirements:
                    <div class="indent">
                        <div class="small-light-text">No requirements for this project.</div>
                    </div>
                % else:
                    % for requirement in requirements:
                        <div class="inner-container">
                            <div class="indent">
                                <a href="/requirement?requirement_id=${requirement['id']}">${requirement['name']}</a>
                                <div class="extra-small-light-text"> opened by ${requirement['owner']} on ${requirement['created']}</div>
                            </div>
                        </div>
                    % endfor
                % endif 
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box">
                <div class="box-title">
                    Tickets
                    <div class="right">
                        <a href="/newticket">New</a>
                    </div>
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for ticket in tickets:
                        <div class="inner-container">
                            <div class="indent">
                                <a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                                <div class="extra-small-light-text"> opened by ${ticket['owner']} on ${ticket['created']}</div>
                            </div>
                        </div>
                    % endfor
                % endif
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box">
                <div class="box-title">
                    Notes
                    <div class="right">
                        <a href="/newnote">New</a>
                    </div>
                </div>
                % if not notes:
                    <div class="indent">
                        <div class="small-light-text">No notess for this project.</div>
                    </div>
                % else:
                    % for note in notes:
                        <div class="inner-container">
                            <div class="indent">
                                <a href="/note?ticket_id=${note['id']}">${note['title']}</a>
                                <div class="extra-small-light-text"> opened by ${note['owner']} on ${note['created']}</div>
                            </div>
                        </div>
                    % endfor
                % endif
            </div>
        </div>
    </div>

    % endif
