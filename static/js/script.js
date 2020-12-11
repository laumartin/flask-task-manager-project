$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
        // This are built-in options to customize the datepicker element from Materialize
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
    /* Materialize will generate an unordered-list <ul> using a unique ID that's targeted to our original <select> element.
    Using their JavaScript files, the <input> that we see on screen will populate the <ul> and <li> elements, based on a 'click' event listener.
    As a result, the 'required' attribute from our <select> element on add_task.html doesn't work on unordered-lists, only form elements, 
    which is why that form validation this gets ignored. To avoid this, we use the following jquery scripts*/
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        // Setting two new variables for some CSS styles, that will match the Materialize validation. One for being valid green, and one for invalid, red
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        // if any select element has the property of 'required', then we need to un-hide it, but make it virtually invisible without any width or height.
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            //Once a user is focused within the <input> on screen, we'll traverse the DOM,using the parent and children selectors with event listeners.
            $(this).parent(".select-wrapper").on("change", function () {
                // If one of the list-items is selected, but doesn't have the 'disabled class for our default item, we'll apply styles to make it valid and green.
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            // we'll apply a green valid class again, if there isn't either the valid or invalid classes, based on the same DOM traversing above
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                /* when the user comes out of the selection, and the bottom-border wasn't updated to valid green, then they've not properly selected anything.
                we'll apply the invalid red class to the input.*/
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
  });