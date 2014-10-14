<%inherit file="base.mak"/>

    % if project == None:
        <script>
            window.location.href = "/?token=${token}"
        </script>
    % endif

    % if user and token and project:
    <div class="row">
        <div class="medium-12 columns">
        </div>
    </div>
    % endif
