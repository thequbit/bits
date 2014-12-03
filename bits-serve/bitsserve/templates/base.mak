<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <link rel="icon" type="image/png" href="static/media/favicon.png">

    <title>bits - Requirements and Ticketing System</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'> 
    
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    <link rel="stylesheet" href="static/foundation/css/foundation-datepicker.css" />
    
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    
    <style>

        
        % if user:

            % if user.theme == 'light':

                /* -- default theme (light) -- */

                body {
                    font-family: 'Lato', sans-serif !important;
                }

                div.title-bar {
                    background-color: rgba(0,140,186,0.2) !important;
                }
                
            % else:
            
                /* -- dark theme  -- */
            
                body {
                    color: #CCCCCC !important;
                    background-color: #050505 !important;
                    font-family: 'Lato', sans-serif !important;
                }
                
                h1, h2, h3, h4, h5, h6, h7, h8, h9 {
                    color: #CCCCCC !important;
                }
                
                input, textarea {
                    color: #CCCCCC !important;
                    background-color: #202020 !important;
                }
                
                div.title-bar {
                    background-color: rgba(0,140,186,0.6) !important;
                }
                
            % endif

        % endif
        
        
        
        div.manage-link {
            margin-top: 10px;
        }
        
        div.page-title h4 {
            padding-top: 6px;
        }
        
        a.extra-small-button {
            /*padding: 0.875rem 1.00rem 0.9375rem !important;*/
            
        }

        div.shrink {
            display: inline-block;
        }

        div.task-title {
            color: rgba(0,255,0,0.8);
            display: inline-block;
        }

        div.task-title a {
            color: rgba(0,255,0,0.8) !important;
        }


        div.ticket-title {
            color: rgba(255,0,0,0.8);
            display: inline-block;
        }

        div.ticket-title a {
            color: rgba(255,0,0,0.8) !important;
        }


        div.list-title {
            color: rgba(0,0,255,0.8);
            display: inline-block;
        }

        div.list-title a {
            color: rgba(0,0,255,0.8) !important;
        }


        div.requirement-title {
            color: rgba(64,64,128,0.8);
            display: inline-block;
        }

        div.requirement-title a {
            color: rgba(64,64,128,0.8) !important;
        }


        div.milestone-title {
            color: rgba(64,128,64,0.8);
            display: inline-block;
        }

        div.milestone-title a {
            color: rgba(64,128,0,08) !important;
        }  


        div.note-title {
            color: rgba(128,64,64,0.8);
            display: inline-block;
        }

        div.note-title a {
             color: rgba(128,64,64,0.8) !important;
         }

        div.top-links a {
            #margin-left: 10px;
            margin-left: 10px !important;
        }

        aside.side-menu {
            border-left: 1px solid #DDD;
        }

        textarea {
            min-height: 150px;
        }

        div.padded-bottom {
            padding-bottom: 6px;
        }

        div.shadow {
            box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);
        }

        div.error-box {
            color: red;
            font-weight: bold;
        }

        div.markdown-text {
            padding-top: 8px; padding-right: 2px;
        }

        div.top-border {
            padding-top: 3px;
            border-top: 1px solid #DDD;
        }

        div.bottom-border {
            padding-bottom: 6px;
            border-bottom: 1px solid #DDD;
        }

        div.left-border {
            padding-left: 3px;
            border-left: 1px solid #DDD;
        }

        div.right-border {
            padding-right: 3px;
            border-right: 1px solid #DDD;
        }

        div.normal-text {
            font-size: 150%;
        }

        div.small-text {
            font-size: 80%;
        }

        div.light-text {
            color: #DDD;
        }

        div.small-light-text {
            font-size: 80%;
            color: #BBB;
        }

        div.extra-small-light-text {
            font-size: 60%;
            color: #BBB;
        }

        div.list-container {
            min-height: 342px;
        }

        div.box {
            /*background-color: white !important;*/
            margin-top: 20px;
            padding: 5px;
            /*border: 1px solid #DDD;*/
            #border-radius: 4px;
        }

        div.box h6 {
            margin-bottom: 0px;
        }

        div.box-title {
            margin-bottom: 8px;
            border-bottom: 1px solid #DDD;
            #border-top-left-radius: 4px;
            #border-rop-right-radius: 4px;
            padding-bottom: 2px;
        }

        div.box-inner-container {
            border-bottom: 1px solid #DDD;
            margin-bottom: 10px;
            margin-left: 20px;
            margin-right: 20px;
            padding-bottom: 10px;
        }

        div.container-inner {
            padding: 10px;
        }

        div.container-inner p {
            margin-bottom: 0px !important;
        }

        div.short-line-height {
            line-height: 100% !important;
        }

        div.small-text {
            font-size: 80% !important;
        }
        
        /*
        div.small-text a {
            font-size: 80% !important;
        }
        */
        
        div.box-small-text {
            font-size: 80%;
        }

        div.box-small-text b {
            padding-right: 5px;
        }

        div.block-container {
            border: 1px solid #DDD;
            border-radius: 2px;
        }

        div.block-contents {
            padding: 10px;
        }

        div.block-contents-inner {
            margin-top: 5px;
            padding: 5px;
            border: 1px solid #F9F9F9;
        }
        
        div.block-type {
            color: white;
            margin-top: 5px;
            margin-bottom: 10px;
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

        div.indent {
            padding-left: 20px;
        }  
 
        div.indent-right {
            padding-right: 20px;
        }
 
        div.title-bar {
            width: 100%;
            border-bottom: 1px solid #DDD;
            margin-bottom: 10px;
            
        }

        div.title-bar h3 {
            margin-bottom: 0.15rem !important;
        }

        div.action-box {
            /* background-color: white; */
            padding: 10px;
            font-size: 90%;
            margin-top: 10px;
        }

        div.action-box p {
            /*color: #BBB;*/
            /*margin-top: 10px;*/
            /*font-size: 70%;*/
            /*padding-left: 5px;*/
            margin-bottom: 0px !important;
        }

        div.assignment-box {
            /* background-color: white; */
            padding: 10px;
            font-size: 90%;
            margin-top: 10px;
        }

        div.assignment-box p {
            /*color: #BBB;*/
            /*margin-top: 10px;*/
            /*font-size: 70%;*/
            /*padding-left: 5px;*/
            margin-bottom: 0px !important;
        }

        input[type="checkbox"] {
            margin: 0px 0px 0.5rem;
            margin-right: 8px !important;
            
        }
    
        div.box h5 {
            margin-bottom: 0px;
        }
        
        div.error-field {
            font-size: 70%;
            padding-left: 5px;
            color: #FFF;
            background-color: #F04124;
        }
        
        div.task-container {
            border-bottom: 1px solid #DDD;
            padding-bottom: 5px;
        }
        
        div.task-container h3 {
            margin-bottom: 0rem !important;
        }

        div.task {
            margin-top: 10px;
            border: 1px solid #DDD;
            padding: 15px;15px
        }

        textarea {
           min-height: 150px;
        }

        

        div.comment-container {
            
        }

        div.container-inner {
            padding: 10px;            
        }
        
        div.container-inner p {
            margin-bottom: 0px !important;
        }
        
        h4.complete-label {
            margin-left: 20px;
            color: #008000;
            font-weight: bold;
        }
        
        div.due-label {
            padding-top: 10px;
        }
        
        div.ticket-container {
            border-bottom: 1px solid #DDD;
            padding-bottom: 5px;
        }
        
        div.ticket-container h3 {
            margin-bottom: 0rem !important;
        }

        div.ticket {
            margin-top: 10px;
            border: 1px solid #DDD;
            padding: 15px;15px
        }

        textarea {
           min-height: 150px;
        }

        

        div.comment-container {
            
        }

        div.container-inner {
            padding: 10px;            
        }
        
        div.container-inner p {
            margin-bottom: 0px !important;
        }
        
        h4.closed-label {
            margin-left: 20px;
            color: red;
            font-weight: bold;
        }

        div.edit-link {
            margin-bottom: 10px !important;
        }

        #submit-ticket {
            margin: 0px !important;
        }
 
        div.inner-container {
            margin-bottom: 10px;
        }

        div.inner-container .extra-small-light-text {
            line-height: 75% !important;
        }

        div.project-description {
            padding: 10px;
        }
        
        div.disabled {
            opacity: .25;
        }
        
        input.single-input {
            width: 90%;
            margin-bottom: 10px;
        }
        
        div.top-bottom-border {
            border-top: 1px solid #008CBA;
            border-bottom: 1px solid #008CBA;
            margin-bottom: 10px;
        }

    </style>

</head>
<body>

    % if user == None:

        <script>
            window.location.href = "/login";
        </script>

    % else:

        <div class="title-bar"> 
            <div class="row">
                <div class="large-12 columns">
                    <h3>bits
                        <small>
                            <a href="/settings">Settings</a>
                        </small>
                    </h3>
                </div>
            </div>
        </div>
        
        <script src="static/foundation/js/vendor/jquery.js"></script>
       
        <div class="row">
             <div class="large-12 columns">
                ${self.body()}
            </div>
        </div>
    
        
        <script src="static/foundation/js/foundation/foundation.js"></script>
        
        <script src="static/foundation/js/foundation/foundation.dropdown.js"></script>

        <script src="static/foundation/js/vendor/modernizr.js"></script>

        <script src="static/foundation/js/foundation-datepicker.js"></script>

        <script>
            $(document).foundation({
                dropdown: {
                    // specify the class used for active dropdowns
                    active_class: 'open'
                }
            });
        </script>
    
    % endif
    
</body>
</html>
