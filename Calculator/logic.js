var current = "0";

const buttonclr = document.getElementById("clear-all");
const buttonOpenBracket = document.getElementById("open-bracket");
const buttonCloseBracket = document.getElementById("close-bracket");
const buttonDivide = document.getElementById("/");
const buttonMultiply = document.getElementById("x");
const buttonSubtract = document.getElementById("-");
const buttonAdd = document.getElementById("+");
const buttonEqual = document.getElementById("=");
const answer = document.getElementById("answer");
const currentvalue = document.getElementById("currentValue");

// Number buttons
for (let i = 0; i < 10; i++) {
    const buttoni = document.getElementById(i.toString());
    if (buttoni) {
        buttoni.onclick = () => click(i);
    }
}

function click(num) {
    if (current === "0") current = ""; // Remove leading zero
    current += num;
    updateDisplay();
}

// Operators
buttonAdd.onclick = () => { current += "+"; updateDisplay(); };
buttonSubtract.onclick = () => { current += "-"; updateDisplay(); };
buttonMultiply.onclick = () => { current += "x"; updateDisplay(); }; 
buttonDivide.onclick = () => { current += "÷"; updateDisplay(); };
buttonCloseBracket.onclick = () => { current += ")"; updateDisplay(); };
buttonOpenBracket.onclick = () => { current += "("; updateDisplay(); };
buttonEqual.onclick = () => {
    updateDisplay();
    currentvalue.innerText= answer.innerText;
    answer.innerText = "";
};

buttonclr.onclick = () => {
    current = "0";
    ans = "0";
    updateDisplay();
};

function updateDisplay() {
    currentvalue.innerText = current;
    answer.innerText = evaluate(current);
}
function evaluate(expression) {
    // Remove spaces and validate input
    expression = expression.replace(/\s+/g, '');
    expression = expression.replace(/÷/g, "/").replace(/x/g, "*");
    if (!expression.match(/^[0-9+\-*/().]+$/)) return "Invalid Expression";

    try {
        return new Function(`return ${expression}`)();
    } catch (error) {
        return current;
    }
}