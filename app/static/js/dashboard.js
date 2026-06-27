// ======================================================
// FinGuard AI Dashboard
// ======================================================

const form = document.getElementById("predictionForm");

const resultDiv = document.getElementById("result");

// ===========================================
// Store Latest Batch Prediction
// ===========================================

let latestCSVResults = [];

let originalCSVData = [];

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    resultDiv.innerHTML = "<h3>Analyzing Transaction...</h3>";

    const transaction = {

        step: Number(
            document.getElementById("step").value
        ),

        type:
            document.getElementById("type").value,

        amount: Number(
            document.getElementById("amount").value
        ),

        oldbalanceOrg: Number(
            document.getElementById("oldbalanceOrg").value
        ),

        newbalanceOrig: Number(
            document.getElementById("newbalanceOrig").value
        ),

        oldbalanceDest: Number(
            document.getElementById("oldbalanceDest").value
        ),

        newbalanceDest: Number(
            document.getElementById("newbalanceDest").value
        )

    };

    try{

        const response = await fetch(

            "/predict",

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },

                body:JSON.stringify(transaction)

            }

        );

        const data = await response.json();

        showResult(data);

    }

    catch(error){

        resultDiv.innerHTML=

        "<h3 style='color:red'>Prediction Failed</h3>";

        console.log(error);

    }

});

// ======================================================
// Display Prediction Result
// ======================================================

function showResult(data){
    document.getElementById("analyticsSection").style.display = "none";

    let color = "#22c55e";

    if(data.prediction === "Fraud"){

        color = "#ef4444";

    }

    else if(data.risk_level === "Medium"){

        color = "#f59e0b";

    }

    let reasonsHTML = "";

    data.reasons.forEach(reason => {

        reasonsHTML += `

            <li>${reason}</li>

        `;

    });

    resultDiv.innerHTML = `

        <div class="result-card">

            <h2 style="color:${color};">

                ${data.prediction}

            </h2>

            <hr>

            <p>

                <strong>Fraud Probability :</strong>

                ${data.fraud_probability} %

            </p>

            <p>

                <strong>Genuine Probability :</strong>

                ${data.genuine_probability} %

            </p>

            <p>

                <strong>Confidence :</strong>

                ${data.confidence} %

            </p>

            <p>

                <strong>Risk Level :</strong>

                <span style="color:${color};font-weight:bold;">

                    ${data.risk_level}

                </span>

            </p>

            <p>

                <strong>Timestamp :</strong>

                ${data.timestamp}

            </p>

            <hr>

            <h3>

                Explanation

            </h3>

            <ul>

                ${reasonsHTML}

            </ul>

        </div>

    `;

}

// ======================================================
// Display CSV Results
// ======================================================

function displayCSVResults(data){

    if(data.error){

        resultDiv.innerHTML = `

            <h2 style="color:red;">

                ${data.error}

            </h2>

        `;

        return;

    }

    latestCSVResults = data.results;
    updateAnalytics(data);

    let fraud = 0;

    let genuine = 0;

    let table = `

    <h2>Batch Prediction Results</h2>

    <table class="result-table">

    <tr>

        <th>#</th>

        <th>Prediction</th>

        <th>Fraud %</th>

        <th>Risk</th>

    </tr>

    `;

    data.results.forEach((item,index)=>{

        if(item.prediction==="Fraud")

            fraud++;

        else

            genuine++;

        table += `

        <tr>

            <td>${index+1}</td>

            <td>${item.prediction}</td>

            <td>${item.fraud_probability}%</td>

            <td>${item.risk_level}</td>

        </tr>

        `;

    });

    table += `

    </table>

    <br>

    <h3>

    Total : ${data.total_transactions}

    </h3>

    <h3>

    Fraud : ${fraud}

    </h3>

    <h3>

    Genuine : ${genuine}

    </h3>

    <br>

    <button

        class="predict-btn"

        onclick="downloadCSV()"

    >

        Download CSV Report

    </button>

    `;

    resultDiv.innerHTML = table;

}

// ======================================================
// CSV Upload
// ======================================================

const uploadBtn = document.getElementById("uploadBtn");

const csvFile = document.getElementById("csvFile");

uploadBtn.addEventListener("click", async () => {

    if (csvFile.files.length === 0) {

        alert("Please select a CSV file.");

        return;

    }

    const formData = new FormData();

    const file = csvFile.files[0];

    formData.append("file", file);

    resultDiv.innerHTML = `

        <h3>

            Processing CSV...

        </h3>

    `;

    // ===========================================
// Read Original CSV
// ===========================================

const text = await file.text();

const rows = text.trim().split("\n");

const headers = rows[0].split(",");

originalCSVData = [];

for(let i=1;i<rows.length;i++){

    const values = rows[i].split(",");

    let obj = {};

    headers.forEach((header,index)=>{

        obj[header.trim()] = values[index];

    });

    originalCSVData.push(obj);

}

    try {

        const response = await fetch(

            "/predict-csv",

            {

                method: "POST",

                body: formData

            }

        );

        const data = await response.json();

        displayCSVResults(data);

    } catch (error) {

        console.log(error);

        resultDiv.innerHTML = `

            <h3 style="color:red;">

                CSV Prediction Failed

            </h3>

        `;

    }

});

// ==========================================
// Dashboard Navigation
// ==========================================

// ==========================================
// Dashboard Navigation
// ==========================================

const manualBtn = document.getElementById("manualBtn");
const csvBtn = document.getElementById("csvBtn");

const manualSection = document.getElementById("manualSection");
const csvSection = document.getElementById("csvSection");

manualBtn.addEventListener("click", () => {

    manualBtn.classList.add("active");
    csvBtn.classList.remove("active");

    window.scrollTo({

        top: manualSection.offsetTop - 80,

        behavior: "smooth"

    });

});

csvBtn.addEventListener("click", () => {

    csvBtn.classList.add("active");
    manualBtn.classList.remove("active");

    window.scrollTo({

        top: csvSection.offsetTop - 80,

        behavior: "smooth"

    });

});

// ======================================================
// Download Complete CSV Report
// ======================================================

function downloadCSV(){

    if(latestCSVResults.length===0){

        alert("No prediction results available.");

        return;

    }

    let csv =

`Step,Type,Amount,OldBalanceOrg,NewBalanceOrig,OldBalanceDest,NewBalanceDest,Prediction,Fraud Probability,Genuine Probability,Confidence,Risk Level,Timestamp\n`;

    for(let i=0;i<latestCSVResults.length;i++){

        const original = originalCSVData[i];

        const prediction = latestCSVResults[i];

        csv +=
`${original.step},${original.type},${original.amount},${original.oldbalanceOrg},${original.newbalanceOrig},${original.oldbalanceDest},${original.newbalanceDest},${prediction.prediction},${prediction.fraud_probability},${prediction.genuine_probability},${prediction.confidence},${prediction.risk_level},"${prediction.timestamp}"\n`;

    }

    const blob = new Blob(

        [csv],

        {

            type:"text/csv"

        }

    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;

    link.download = "FinGuard_AI_Report.csv";

    link.click();

    URL.revokeObjectURL(url);

}

// ======================================================
// Analytics Dashboard
// ======================================================

let fraudChart = null;

let riskChart = null;

function updateAnalytics(data){
    
    document.getElementById("analyticsSection").style.display = "block";

    if(data.error){

        return;

    }

    const total = data.total_transactions;

    let fraud = 0;

    let genuine = 0;

    let low = 0;

    let medium = 0;

    let high = 0;

    data.results.forEach(item=>{

        if(item.prediction==="Fraud")

            fraud++;

        else

            genuine++;

        if(item.risk_level==="Low")

            low++;

        else if(item.risk_level==="Medium")

            medium++;

        else

            high++;

    });

    document.getElementById("totalTransactions").innerHTML = total;

    document.getElementById("fraudCount").innerHTML = fraud;

    document.getElementById("genuineCount").innerHTML = genuine;

    document.getElementById("fraudRate").innerHTML =

        ((fraud/total)*100).toFixed(2)+"%";

    createFraudChart(fraud,genuine);

    createRiskChart(low,medium,high);

}

// ======================================================
// Fraud vs Genuine Chart
// ======================================================

function createFraudChart(fraud, genuine){

    const ctx = document.getElementById("fraudChart");

    if(fraudChart){

        fraudChart.destroy();

    }

    fraudChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[

                "Fraud",

                "Genuine"

            ],

            datasets:[{

                data:[

                    fraud,

                    genuine

                ],

                backgroundColor:[

                    "#ef4444",

                    "#22c55e"

                ],

                borderWidth:2

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    position:"bottom",

                    labels:{

                        color:"white"

                    }

                }

            }

        }

    });

}

// ======================================================
// Risk Distribution Chart
// ======================================================

function createRiskChart(low, medium, high){

    const ctx = document.getElementById("riskChart");

    if(riskChart){

        riskChart.destroy();

    }

    riskChart = new Chart(ctx,{

        type:"bar",

        data:{

            labels:[

                "Low",

                "Medium",

                "High"

            ],

            datasets:[{

                label:"Transactions",

                data:[

                    low,

                    medium,

                    high

                ],

                backgroundColor:[

                    "#22c55e",

                    "#f59e0b",

                    "#ef4444"

                ]

            }]

        },

        options:{

            responsive:true,

            scales:{

                x:{

                    ticks:{

                        color:"white"

                    },

                    grid:{

                        color:"#334155"

                    }

                },

                y:{

                    beginAtZero:true,

                    ticks:{

                        color:"white"

                    },

                    grid:{

                        color:"#334155"

                    }

                }

            },

            plugins:{

                legend:{

                    labels:{

                        color:"white"

                    }

                }

            }

        }

    });

}