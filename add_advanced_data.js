const fs = require('fs');
const https = require('https');

const JS_FILE = '/Users/pochoco/Desktop/원소주기율표/elements_data.js';
const URL = 'https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json';

console.log("Downloading advanced data...");

https.get(URL, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
        const data = JSON.parse(body);
        const elementsDict = {};
        
        data.elements.forEach(el => {
            elementsDict[el.number] = {
                density: el.density || null,
                electronegativity: el.electronegativity_pauling || null,
                electron_config: el.electron_configuration_semantic || '',
                shells: el.shells ? el.shells.join(', ') : '',
                discovered_by: el.discovered_by || '',
                named_by: el.named_by || '',
                appearance: el.appearance || '',
                molar_heat: el.molar_heat || null,
                electron_affinity: el.electron_affinity || null,
                ionization_energies: el.ionization_energies ? el.ionization_energies[0] : null,
                summary: el.summary || '',
                spectral_img: el.spectral_img || ''
            };
        });

        console.log("Reading elements_data.js...");
        let jsContent = fs.readFileSync(JS_FILE, 'utf-8');
        
        // Extract array
        const match = jsContent.match(/const elementsData = (\[[\s\S]*\]);/);
        if (!match) {
            console.error("Could not find elementsData array in JS file.");
            process.exit(1);
        }
        
        // Eval to parse as JS object
        let elementsData;
        eval('elementsData = ' + match[1]);
        
        // Update data
        elementsData.forEach(el => {
            const advanced = elementsDict[el.num];
            if (advanced) {
                el.density = advanced.density;
                el.electronegativity = advanced.electronegativity;
                el.electron_config = advanced.electron_config;
                el.shells = advanced.shells;
                el.discovered_by = advanced.discovered_by;
                el.named_by = advanced.named_by;
                el.appearance = advanced.appearance;
                el.molar_heat = advanced.molar_heat;
                el.electron_affinity = advanced.electron_affinity;
                el.ionization_energies = advanced.ionization_energies;
                el.summary = advanced.summary;
                el.spectral_img = advanced.spectral_img;
            }
        });
        
        // Serialize back
        const newJsContent = jsContent.replace(
            match[1], 
            JSON.stringify(elementsData, null, 2)
        );
        
        fs.writeFileSync(JS_FILE, newJsContent, 'utf-8');
        console.log("Successfully injected advanced data into elements_data.js!");
    });
}).on('error', (e) => {
    console.error(e);
});
