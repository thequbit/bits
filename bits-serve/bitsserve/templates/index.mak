<%inherit file="base.mak"/>

    % if user and token:

    <div class="row">
        <div class="medium-12 columns">
            <!--
            <div class="indent">
                <h4>Welcome ${user.first} ${user.last}</h4>
            </div>
            -->
            <h3>Projects</h3>
            % for project in projects:
                <div class="block-container">
                    <div class="block-title">
                        <a href="/project?token=${token}&project_id=${project['id']}">${project['name']}</a>
                    </div>
                    <div class="block-contents">
                        <p class="small">
                            Created: September 5th, 2011<br/>
                            Owner: Tim Duffy
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
            % endfor
            <hr/> 
        </div>
    </div>

    % endif

