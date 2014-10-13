<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <title>bits - Requirements and Ticketing System</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css"> 
    
    <!--<script src="//code.jquery.com/jquery-1.10.2.js"></script>-->
    
    
    <style>
    
        div.top-links {
            border-bottom: 1px solid #DDD;
        }
    
    </style>

</head>
<body>

    <div class="row">
        <div class="large-12 columns">
            <div class="right">
                <h4><div id="current-organization"></div><small><div id="current-project"></div></small></h4>
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
                <li><a href="#">New Project</a></li>
                <li><a href="#">New Ticket</a></li>
                <li><a href="#">New Note</a></li>
                <li style="border-bottom: 1px solid #DDD;"><a href="#"></a></li>
                <li><a href="#">Settings</a></li>
                <li><a href="#">Help</a></li>
            </ul>
        </aside>
        <div class="large-10 columns">
            ${self.body()}
        </div>
    </div>
    
    
    

</body>
</html>
