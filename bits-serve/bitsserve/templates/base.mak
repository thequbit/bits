<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <title>bits - Requirements and Ticketing System</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'> 
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    
    <style>

        a.extra-small-button {
            /*padding: 0.875rem 1.00rem 0.9375rem !important;*/
            
        }

        div.indent {
            padding-left: 20px;
        }

        div.double-indent {
            padding-left: 40px;
        }

        div.tripple-indent {
            padding-left: 60px;
        }

        div.block-container {
            border: 1px solid #DDD;
            border-radius: 8px;
        }

        div.block-title {
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding-left: 10px;
            background-color: #DDD;
            color: #333;
            border-bottom: 1px solid #DDD;
        }

        div.block-contents {
            padding: 10px;
        }

        p.small {
            font-size: 60%;
            margin-bottom: 0px !important;
        }

        div.inner-block-contents {
            padding: 4px;
            border: solid 1px #F9F9F9;
        }

        div.block-type {
            color: white;
            margin-top: 10px;
            padding-left: 6px;
            padding-top: 2px;
            padding-bottom: 2px;
            padding-right: 6px;
            border-radius: 8px;
            display: inline-block;
        }

        div.block-type a {
            color: white !important;
        }


    </style>



</head>
<body>

    % if token == None or user == None:
        <script>
            window.location.href = "/login";
        </script>
    % endif

    <script>
        // make sure we are logged in
        if( localStorage.token == '' || localStorage.token == undefined ) {
            window.location.href = "/login";
        }
    </script>

    <div class="row">
        <div class="large-12 columns">
            <div class="right">
                % if user != None:
                <h4>${user.first} ${user.last} 
                    % if project:
                    <small>${project['name']}</small>
                    % endif
                </h4>
                % endif
            </div>
            <h2>bits</h2>
            <hr/>
        </div>
    </div>

    <script src="static/foundation/js/vendor/jquery.js"></script>
    <script src="static/foundation/js/foundation.min.js"></script>
    <script src="static/foundation/js/vendor/modernizr.js"></script>

    <script>
        $(document).foundation();
    </script>
    
    <div class="row">
        
        <aside class="large-2 columns" style="border-right: 1px solid #DDD;">
            <ul class="side-nav">
                <!--<li><a href="/?token=${token}">Home</a></li>-->
                <li><a href="/?token=${token}">Projects</a></li>
                <!--
                <li><a href="/newrequirement?token=${token}">New Requirement</a></li>
                <li><a href="/newtickets?token=${token}">New Ticket</a></li>
                <li><a href="/newnote?token=${token}">New Note</a></li>
                -->
                <!--<li style="border-bottom: 1px solid #DDD;"><a href="#"></a></li>-->
                <hr/>
                <li><a href="/settings">Settings</a></li>
                <li><a href="/help">Help</a></li>
                <hr/>
            </ul>
        </aside>
        <div class="large-10 columns">
            ${self.body()}
        </div>
    </div>
    
    
    

</body>
</html>
