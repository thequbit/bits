<%inherit file="base.mak"/>

    <div class="row">
        <div class="large-12 columns bottom-border">
            
            <a href="/">Home</a>
             > 
            Projects
            
        </div>
    </div>

    <div class="row">
        <div class="medium-12 column">
            
            % for project in projects:
                     
                <div class="box shadow project-container">
                    <div class="box-inner-container">
                        <h5><a href="/project?project_id=${project['id']}">${project['name']}</a></h5>
                        <div class="container-inner">
                            ${project['description']}
                        </div>
                    </div>
                </div>
                
            % endfor
            
        </div>
    </div>
