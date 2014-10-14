<%inherit file="base.mak"/>

    <style>
    
        div.actions-feed {
        }

        div.action-box {
            padding: 10px;
            border-top: 1px solid #DDD;
        }

        div.action-box {
        /*    box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);*/
            margin-bottom: 20px;
        }

        div.action-box p {
            color: #BBB;
            margin-top: 10px;
            font-size: 70%;
            padding-left: 20px;
        }

        div.small-light-text {
            font-size: 80%;
            color: #BBB;
        }

        /*
        div.box {
            padding: 5px;
            border: 2px solid #DDD;
            border-radius: 4px;
        }
        
        div.box-title {
            margin-bottom: 6px;
            border-bottom: 2px solid #DDD;
            border-top-left-radius: 4px;
            border-rop-right-radius: 4px;
            padding-bottom: 2px;
        }

        div.box-small-text {
            font-size: 80%;
        }
        
        div.box-small-text b {
            padding-right: 5px;
        }

        div.indent {
            padding-left: 20px;
        }
        */

    </style>

    % if user and token and projects:

    <div class="row">
        <div class="medium-8 columns">
        
            <h5>Actions Feed<h5>
            <div class="row">
                        <div class="small-10 columns">
                            <div class="action-box shadow">
                                <div class="small-light-text">10 Minutes ago</div>
                                <a href="/user?user_id=1">Tim Duffy</a>
                                Created a new ticket in 
                                <a href="/project?project_id=1">House Stuff</a>
                                <p>The front of the garage needs to be cleaned</p>
                            </div>

                            <div class="action-box shadow">
                                <div class="small-light-text">1 Hour ago</div>
                                <a href="/user?user_id=1">Tim Duffy</a>
                                Created a new requirement in
                                <a href="/project?project_id=1">House Stuff</a>
                                <p>The outside of the house shall be clean before the first snow</p>
                            </div>
                        </div>
            </div>
        </div>

        <div class="medium-4 columns">
            <div class="row">
            <div class="medium-12 columns">
            <div class="box shadow">
                <div class="box-title">
                    Current Projects
                    <div class="right">
                        <a href="/newproject">New Project</a>
                    </div>
                </div>
                % for project in projects:
                <div class="indent">
                    <a href="/project?project_id=${project['id']}">${project['name']}</a>        
                    <div class="right">
                        <div class="box-small-text">r:<b>${project['requirement_count']}</b>t:<b>${project['ticket_count']}</b>n:<b>${project['note_count']}</b></div>
                    </div>
                </div>
                % endfor
            </div>
            <hr/>

        </div>

    </div>

    % endif

