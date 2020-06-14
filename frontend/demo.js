

const url_ananlysis = "http://localhost:5000/aspect_sentiment_analysis"

// function getColor(str) {
//   switch(str){
//     case "O":
//       color = "#333333";
//       break;
//     case "B-LOC":
//       color = "#4285f4";
//       break;
//     case "B-ORG":
//       color = "#32CD32";
//       break;
//     case "I-LOC":
//       color = "#0000CD";
//       break;
//     case "B-PER":
//       color = "#8B0000";
//       break;
//     case "I-PER":
//       color = "#CD5C5C";
//       break;
//     case "I-ORG":
//       color = "#2E8B57";
//       break;
//     case "B-MISC":
//       color = "#FFFF00";
//       break;
//     case "I-MISC":
//       color = "#FFA500";
//       break;
//     case "N":
//       color = "red";
//       break;
//     case "M":
//       color = "#333333";
//       break;
//     }
//   return color
// }

function insertResult(sentence) {
  sen = '<div class="d-flex justify-content-around">'
  len = sentence.category.length
  console.log(sentence.category[0])
  console.log(len)
  // console.log(sentence)
  var i
  x = ''
  for (i = 0; i < len; i++){
    if(sentence.polarity[i] == 'negative'){
      sen += '<button type="button" class="btn btn-danger">'
      x = sentence.category[i] + ': '
      x += sentence.polarity[i] + '<br />'
      sen += x
    }
    else if(sentence.polarity[i] == 'positive'){
      sen += '<button type="button" class="btn btn-success">'
      x = sentence.category[i] + ': '
      x += sentence.polarity[i] + '<br />'
      sen += x
    }
    else if(sentence.polarity[i] == 'neutral'){
      sen += '<button type="button" class="btn btn-info">'
      x = sentence.category[i] + ': '
      x += sentence.polarity[i] + '<br />'
      sen += x
    }
    sen += '</button>'
  }
  sen += '</div>'
  console.log(sen)
  resultEle.innerHTML = sen
  // console.log(x)
}

async function analysis() {
  /*
    demo
  */
  // sentence = {
  // "category":["service", "food", "prize"],
  // "polarity": ["negative", "positive", "neutral"]
  // }
  // console.log('annalysis')
  // btnSubmit.style.display = "none"
  // btnReset.style.display = "flex"
  // insertResult(sentence)


  /*
    run
  */
  const inputValue = inputEle.value
  console.log(inputValue)
  console.log(typeof(inputValue))
  try {
    const response = await axios.post(url_ananlysis, {
      text: inputValue
    });
    console.log('loading')
    if (response.status === 200) {
      console.log(response)
      let data = response.data
      let sentence =  data
      console.log(typeof(sentence))
      console.log(sentence)
      insertResult(sentence)
    }
  } catch (error) {
    console.error(error);
  }
}

function reset() {
  inputEle.value = ""
  btnReset.style.display = "none"
  btnSubmit.style.display = "flex"
  resultEle.innerHTML = ""
}

const btnSubmit = document.getElementById('btn-submit')
const btnReset = document.getElementById('btn-reset')
const resultEle = document.getElementById("result")
const inputEle = document.getElementById('input')

const sentence = [
  { text: "ha noi", value: 'N' },
  { text: 'viet nam', value: 'M'}
]

btnSubmit.addEventListener('click', analysis)
btnReset.addEventListener('click', reset)


/*
  @form of data

let data = {
	sentence: [
  	{text: "hom nay", value: 'N' },
    {text: 'troi dep', value: 'M'}
  ]
}

*/

// sentence = {
//   "category":["service", "food", "prize"],
//   "polarity": ["negative", "positive", "neutral"]
// }
// insertResult(sentence)