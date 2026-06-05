import * as fs from 'fs';
import { fileURLToPath } from 'url';
import pdfParse from 'pdf-parse';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const pdfPath = path.join(__dirname, 'neet_2026.pdf'); 

async function readPDF(filename:string):Promise<string>{
    try{

        const dataBuffer =await fs.readFileSync(filename);
        const data = await pdfParse(dataBuffer);
        return data.text;
    }catch(err){
        console.error(`Error reading PDF file: ${err}`);
        throw err;
    }
}


readPDF(pdfPath).then(text => {
    console.log(text);
}).catch(err => {
    console.error(`Error: ${err}`);
}   );