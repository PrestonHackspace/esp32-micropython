import fs = require('fs');
import path = require('path');
import pump = require('pump');
import del = require('del');
import gulp = require('gulp');
import uglify = require('gulp-uglify');
import debug = require('gulp-debug');
import gzip = require('gulp-gzip');
import gulpif = require('gulp-if');

const CorePath = path.join(__dirname, 'board');

const PanelPath = path.join(__dirname, 'panel', 'dist');

const EduBlocksPath = path.join(__dirname, '..', 'edublocks-micropython', 'web');

const dest = path.join(__dirname, 'board-fs');

const ExtNoGzip = ['.py', '.xml', '.mp3', '.wav', '.json']

const compressionStages = () => [
  gulpif((f) => f.extname === '.js', uglify()),
  gulpif((f) => ExtNoGzip.indexOf(f.extname) === -1, gzip({ gzipOptions: { level: 9 } })),
];

gulp.task('clean', () => {
  return del([path.join(dest, '*')]);
});

gulp.task('bundle-core', () => {
  return pump([
    gulp.src([`${CorePath}/**/*.*`], { base: CorePath }),
    debug({ title: 'bundle-core' }),
    ...compressionStages(),
    gulp.dest(dest),
  ]);
});

gulp.task('bundle-panel', () => {
  return pump([
    gulp.src([`${PanelPath}/**/*.*`], { base: PanelPath }),
    debug({ title: 'bundle-panel' }),
    ...compressionStages(),
    gulp.dest(path.join(dest, 'web')),
  ]);
});

gulp.task('bundle-edublocks', () => {
  const assetsJsonPath = path.join(EduBlocksPath, '..', 'assets.json');

  if (!fs.existsSync(assetsJsonPath)) {
    throw new Error('EduBlocks source not found!');
  }

  const assets: string[] = JSON.parse(fs.readFileSync(assetsJsonPath, 'utf-8'));

  const assetPaths = assets.map((asset) => path.join(EduBlocksPath, asset));

  return pump([
    gulp.src(assetPaths, { base: EduBlocksPath }),
    debug({ title: 'bundle-edublocks' }),
    ...compressionStages(),
    gulp.dest(path.join(dest, 'web')),
  ]);
});

gulp.task('default', gulp.series(['clean', 'bundle-core', 'bundle-panel', 'bundle-edublocks']));
