function closeMessageOnClick(id) {
    document.querySelector(id).addEventListener("click", function() {
        this.style.display = "none";
    });
}
  
// function closeMessageAfterTimeout(id) {
//     console.log("Starting timeout for " + id);
//     setTimeout(function() {
//         fadeOut(document.querySelector(id));
//     }, 5000);
// }
  
// function fadeOut(element) {
//     let opacity = 1;
//     const intervalId = setInterval(frame, 50);
  
//     function frame() {
//         if (opacity <= 0) {
//             clearInterval(intervalId);
//             element.style.display = "none";
//         } else {
//             opacity -= 0.1;
//             element.style.opacity = opacity;
//         }
//     }
// }
  
// function progressBar(id) {
//     const element = document.querySelector(id);
//     let width = 0;
//     const intervalId = setInterval(frame, 50);
  
//     function frame() {
//         if (width >= 100) {
//             clearInterval(intervalId);
//         } else {
//             width++;
//             element.style.width = `${width}%`;
//         }
//     }
// }

function detecterForceMotDePasse(motDePasse) {
    let force = 0;

    force+=motDePasse.length;
    if (/\d/.test(motDePasse)) force+=5;
    if (/[\W_]/.test(motDePasse)) force+=5;

    const estSuiteAlphabetique = ["abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba"].some(suite => motDePasse.includes(suite));
    const estSuiteDeChiffres = /(\d)\1{2}/.test(motDePasse);
    const estMotDePasseFaible = ["password", "123456", "12345678", "admin", "qwerty", "abcd1234"].includes(motDePasse.toLowerCase());

    if (!estSuiteAlphabetique && !estSuiteDeChiffres && !estMotDePasseFaible) force+=2;
    if (motDePasse.length < 8) force-=2
        return force;
}

const inputMotDePasse = document.getElementById('signup-password');
const indicateurForceRemplissage = document.getElementById('indicateur-force-remplissage');
indicateurForceRemplissage.style.width = '0%';
inputMotDePasse.addEventListener('input', (event) => {
    const motDePasse = event.target.value;
    const force = detecterForceMotDePasse(motDePasse);

    if (force >= 0 && force <= 9) {
        indicateurForceRemplissage.classList.remove('bg-yellow-500', 'bg-green-500');
        indicateurForceRemplissage.classList.add('bg-red-500');
        let percent = 4.12 * force;
        $(indicateurForceRemplissage).animate({ width: (percent) + '%' }, 200);
    } else if (force >= 10 && force <= 17) {
        let percent = 33 + 4.12 * force;
        if (percent > 66) percent = 66;
        indicateurForceRemplissage.classList.remove('bg-red-500', 'bg-green-500');
        indicateurForceRemplissage.classList.add('bg-yellow-500');
        $(indicateurForceRemplissage).animate({ width: (percent) + '%' }, 200);
    } else {
        let percent = 66 + 4.12 * force;
        if (percent > 100) percent = 100;
        indicateurForceRemplissage.classList.remove('bg-red-500', 'bg-yellow-500');
        indicateurForceRemplissage.classList.add('bg-green-500');
        $(indicateurForceRemplissage).animate({ width: (percent) + '%' }, 200);
    }
});