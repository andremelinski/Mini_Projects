// DATA MODULE
var budgetController = (function () {

    var Expense = function (id, description, value) {
        this.id = id;
        this.description = description;
        this.value = value;
        this.percentage = -1;
    };

    Expense.prototype.calcPercentage = function(totalIncome){

        if(totalIncome>0){
            this.percentage = Math.round((this.value/totalIncome)*100)

        } else{
            this.percentage = -1;
        }
    };

    Expense.prototype.getPercentage = function(){
        return this.percentage;
    }

    var Income = function (id, description, value) {
        this.id = id;
        this.description = description;
        this.value = value;
    };

    var calctotal = (type) =>{    
        var sum = 0;
        data.allItems[type].forEach(cur => {
            sum += cur.value;

        });
        data.totals[type] = sum;
    };

    var data = {

        allItems: {
            exp: [],
            inc: []
        },
        totals: {
            exp: 0,
            inc: 0
        },
        budget: 0,
        percentage: -1
    };

    return {
        addItem: function (type, des, val) {
            var newItem, ID;

            // Creating ID
            if (data.allItems[type].length > 0) {

                ID = data.allItems[type][data.allItems[type].length - 1].id + 1;

            } else {
                ID = 0;
            }

            // ADDING IN THE CORRECT PLACE
            if (type === 'exp') {
                newItem = new Expense(ID, des, val);

            } else if (type === 'inc') {
                newItem = new Income(ID, des, val);
            }
            data.allItems[type].push(newItem); //add in the correct arr
            return newItem;
        },

        calculateBudget: function(){

            // calculate income - expensives
            calctotal("exp");
            calctotal("inc");

            // calculate income - expensives
            data.budget = data.totals.inc - data.totals.exp;

            // calculate % spent
            if(data.totals.inc>0){
                data.percentage = Math.round((data.totals.exp / data.totals.inc)*100);
            }else{ data.percentage = -1};
            
        },

        calculatePercentages: function(){

            data.allItems.exp.forEach(cur => {
                cur.calcPercentage(data.totals.inc);
            });
        },

        getPercentages : function(){
            var allPerc = data.allItems.exp.map(function(cur){
                return cur.getPercentage();
            });
            return allPerc;
        },

        getBudget: function(){
            return {
                budget : data.budget,
                totalInc: data.totals.inc,
                totalExp: data.totals.exp,
                perc: data.percentage
            };
            
        }
    };

})();

// USER INTERFACE MODULE
var userInterface = (function () {
    // Date
    var displayDate = () => {
        var date = new Date();
        var month = date.getMonth();
        var year = date.getUTCFullYear();
        document.querySelector(".budget__title--month").textContent = month + "/" + year;
    }

    var DOMstrings = {
        inputType: ".add__type",
        inputDescription: ".add__description",
        inputValue: ".add__value",
        inputBtn: ".add__btn",
        incomeContainer: ".income__list",
        expensesContainer: ".expenses__list",
        budgetlabel: ".budget__value",
        incomelabel: ".budget__income--value",
        explabel: ".budget__expenses--value",
        perclabel: ".budget__expenses--percentage",
        expensesPercLabel: ".item__percentage"

    }
    return {
        // Date
        date: displayDate(),

        // all values from console
        getinput: function () {
            return {
                type: document.querySelector(DOMstrings.inputType).value, //will be either inc or exp
                description: document.querySelector(DOMstrings.inputDescription).value,
                value: parseFloat(document.querySelector(DOMstrings.inputValue).value),
            };
        },
        addListItem: function(obj, type) {
            var html, newhtml, element; 
            // 1- create html string with a placeholder text
                // 1.2 - fulfil the markers with DOMstrings
            if (type ==="inc"){

                element = DOMstrings.incomeContainer; //add a certain element after incomeContainer
                html='<div class="item clearfix" id="income-%id%"><div class="item__description">%description%</div><div class="right clearfix"><div class="item__value">%value%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>'
            }else if (type === "exp"){

                element = DOMstrings.expensesContainer; //add the html after expensiveContainer
                html = '<div class="item clearfix" id="expense-%id%"><div class="item__description">%description%</div> <div class="right clearfix"> <div class="item__value">%value%</div> <div class="item__percentage">21%</div><div class="item__delete"><button class="item__delete--btn"><i class="ion-ios-close-outline"></i></button></div></div></div>';
            }

            // 2- replace %subjects% to real values
            newhtml = html.replace("%id%", obj.id);
            newhtml = newhtml.replace("%description%", obj.description);
            newhtml = newhtml.replace("%value%", obj.value);

            // 3- Insert the html into DOM
            document.querySelector(element).insertAdjacentHTML("beforeend",newhtml);

        },

        clearFields : function(){
            var fields, arrFields;
            fields = document.querySelectorAll(DOMstrings.inputDescription+", "+ DOMstrings.inputValue);
            arrFields = Array.prototype.slice.call(fields);
            
            arrFields.forEach((currValue, i, arr) => {
                currValue.value = "";
            });

        }, 

        displaybudget : function(obj){
            document.querySelector(DOMstrings.budgetlabel).textContent = obj.budget;            //budget : data.budget,   totalInc: data.totals,       perc: data.percentage
            document.querySelector(DOMstrings.incomelabel).textContent = obj.totalInc;
            document.querySelector(DOMstrings.explabel).textContent = obj.totalExp;

            if(obj.perc>0){
                document.querySelector(DOMstrings.perclabel).textContent = obj.perc+"%";
            }else{
                document.querySelector(DOMstrings.perclabel).textContent = "---";
            }
        },

        displayPercentages: function(percentages){
            
            var fields = document.querySelectorAll(DOMstrings.expensesPercLabel);

            var nodeList = (list,callback) =>{

                for(var i=0; i<list.length; i++){

                    callback(list[i], i);
                }
            };

            nodeList(fields, function(current, index){
                if(percentages[index]>0){

                    current.textContent = percentages[index]+"%";
                }else{
                    current.textContent = "---";
                }
            });
        },


        // classes from HTML
        getDOMstrings: function() {
            return DOMstrings;
        }
    };
}) ();


// CONTROLLER MODULE
var controller = (function (budgetCtr, userInterf) {


    var SetupEvent = function () {
        var DOM = userInterf.getDOMstrings();
        document.querySelector(DOM.inputBtn).addEventListener("click", ctrlAddItem);

        document.addEventListener("keypress", function (event) {
            if (event.keyCode === 13) {
                ctrlAddItem;
            }
        });
    };

    var updateBudget = function(){
        // 1-Calculate
        budgetCtr.calculateBudget();

        // 2-Return bidget
        var budget = budgetCtr.getBudget();
        // 3- Display
        userInterf.displaybudget(budget);
    };

    var updatePercentages = function(){

        //1-Calculate Percentages
        budgetCtr.calculatePercentages();

        // Returnning Percentages
        var percentages = budgetCtr.getPercentages();

        // 3- Display
        userInterf.displayPercentages(percentages);

        
    };

    var ctrlAddItem = function () {
        var input, newItem;
        // 1- Get input data
        input = userInterf.getinput();

        if(input.description!=="" && !isNaN(input.value) && input.value>0) {

            // 2- Add to the budget controller and calculate
            newItem = budgetCtr.addItem(input.type, input.description, input.value);

            // 3- Display info: current money and push to the event 
            userInterf.addListItem(newItem, input.type);

            // 4- Clear the fields 
            userInterf.clearFields();

            // 5- Update budget
            updateBudget();

            // 6- Update percentage
            updatePercentages();
        }
    };

    // Extracting the SetupEvent (init)
    return {
        init: function () {
            console.log("App running");
            SetupEvent();

        }
    };

})(budgetController, userInterface);

controller.init();











