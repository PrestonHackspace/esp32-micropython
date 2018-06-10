import fs = require('fs');
import path = require('path');
import os = require('os');
import shell = require('shelljs');

const SupportedPlatforms = ['darwin', 'linux'];

const checkDependencies = () => {
  const deps = ['ampy'];

  const missing = deps.map((dep) => [shell.which(dep), dep]).filter(([cmd]) => !cmd).map(([cmd, dep]) => dep);

  return missing;
};

const getDirtyFiles = (dir: 'web' | 'py', after?: Date) => {
  const srcDir = path.join(__dirname, '..', 'board', dir);
  const fileNames = fs.readdirSync(srcDir);

  return fileNames.map((fileName) => {
    const filePath = path.join(srcDir, fileName);
    const mtime = fs.statSync(filePath).mtime

    return { fileName, filePath, mtime };
  }).filter(({ fileName, filePath, mtime }) => (fileName[0] !== '.') && (!after || mtime > after));
};

const ls = (port: string) => {
  const result = shell.exec(`ampy -p ${port} ls`, { silent: true });

  if (!('code' in result)) throw new Error('Invalid result');

  if (result.code !== 0) {
    throw new Error('Could not get directory listing');
  }

  return result.stdout.split('\n').filter((file) => !!file);
};

const mkdir = (port: string, path: string) => {
  console.log('==== Creating directory:', path);

  return shell.exec(`ampy -p ${port} mkdir ${path}`).code;
};

const rm = (port: string, path: string) => {
  console.log('==== Removing file:', path);

  return shell.exec(`ampy -p ${port} rm ${path}`).code;
};

const uploadFile = (port: string, src: string, dest: string) => {
  console.log('==== Uploading file:', src, '->', dest);

  return shell.exec(`ampy -p ${port} put ${src} ${dest}`).code;
};

const compressFile = (src: string, dest: string) => {
  console.log('==== Compressing file:', src, '->', dest);

  return shell.exec(`gzip -c ${src} > ${dest}`).code;
};

const uploadPythonScripts = (port: string, lastUpload?: Date) => {
  const scripts = getDirtyFiles('py', lastUpload);

  for (const { fileName, filePath } of scripts) {
    if (fileName === 'boot.py') continue;

    const code = uploadFile(port, filePath, fileName);

    if (code !== 0) {
      console.error('Upload failed');

      throw new Error('Upload failed');
    }
  }
};

const mkdirWebDirIfNotExist = (port: string) => {
  const files = ls(port);

  if (files.indexOf('web') === -1) {
    const mkdirCode = mkdir(port, 'web');

    if (mkdirCode !== 0) {
      console.error('mkdir failed');

      throw new Error('mkdir failed');
    }
  }
};

const uploadWebResources = (port: string, lastUpload?: Date) => {
  // mkdirWebDirIfNotExist(port);

  const gzDir = path.join(__dirname, '..', 'board', 'web.gz');

  const resources = getDirtyFiles('web', lastUpload);

  for (const { fileName, filePath } of resources) {
    const gzFile = `${fileName}.gz`;
    const gzPath = path.join(gzDir, gzFile);

    const compressCode = compressFile(filePath, gzPath);

    if (compressCode !== 0) {
      console.error('Compress failed');

      throw new Error('Compress failed');
    }

    const uploadCode = uploadFile(port, gzPath, `web/${gzFile}`);

    if (uploadCode !== 0) {
      console.error('Upload failed');

      throw new Error('Upload failed');
    }
  }
};

const upload = () => {
  const files = shell.find(path.join(__dirname, '..', 'board', 'web', '*'));

  console.log('files', files.entries());

  process.exit();

  const platform = os.platform();

  if (SupportedPlatforms.indexOf(platform) === -1) {
    console.error('Unsupported platform:', platform);
  }

  const port = os.platform() === 'darwin' ? '/dev/cu.SLAB_USBtoUART' : '/dev/ttyUSB0';

  const deps = checkDependencies();

  if (deps.length) {
    console.error('The following dependencies must be installed first:', deps.join(', '));

    return;
  }

  const lastUploadMarkerFile = path.join(__dirname, '.lastupload');
  const lastUpload = fs.existsSync(lastUploadMarkerFile) ? fs.statSync(lastUploadMarkerFile).mtime : undefined;

  // Remove boot.py so that we don't slow down / crash the upload process
  // rm(port, 'boot.py');

  uploadWebResources(port, lastUpload);

  // uploadPythonScripts(port, lastUpload);

  // Reupload boot.py
  const pyDir = path.join(__dirname, '..', 'board', 'py');

  // uploadFile(port, path.join(pyDir, 'boot.py'), 'boot.py');

  shell.touch(lastUploadMarkerFile);
};

upload();
