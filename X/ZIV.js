const fs = require('fs');
const readline = require('readline');
const { exec } = require('child_process');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('𝐏𝐚𝐬𝐭𝐞 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 𝐓𝐞𝐱𝐭 : ', (teks) => {
  fs.writeFile('XX/MainDecrypt.ziv', teks, (error) => {
    if (error) {
      console.error('Terjadi kesalahan saat menyimpan file:', error);
    } else {
      console.log('File berhasil disimpan.');
      runPythonScript();
    }
  });
});

function runPythonScript() {
  const command = 'python Main.py XX/MainDecrypt.ziv';
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.log(`Error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.log(`Stderr: ${stderr}`);
      return;
    }
    console.log(`Stdout: ${stdout}`);
  });
  rl.close();
}