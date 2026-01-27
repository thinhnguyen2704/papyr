import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, Upload, Loader2 } from 'lucide-react';
import { scanImage } from './services/api';
import { ResultCard } from './components/Result';
import LanguageToggle from './components/LanguageToggle';
import { translations } from './services/translation';

const videoConstraints = {
	width: { min: 640, ideal: 960, max: 2560 },
	height: { min: 360, ideal: 540, max: 1440 },
	facingMode: 'environment',
	focusMode: 'continuous',
};

export default function App() {
	const webcamRef = useRef<Webcam>(null);
	const fileInputRef = useRef<HTMLInputElement>(null);
	const [result, setResult] = useState('');
	const [isScanning, setIsScanning] = useState(false);
	const [copySuccess, setCopySuccess] = useState(false);
	const [language, setLanguage] = useState('en');
	const [darkMode, setDarkMode] = useState(true);
	const t = translations[language];

	const handleCapture = useCallback(async () => {
		if (!webcamRef.current) return;
		const imageSrc = webcamRef.current.getScreenshot();
		if (!imageSrc) return;

		setIsScanning(true);
		try {
			const blob = await fetch(imageSrc).then((r) => r.blob());
			const data = await scanImage(blob, language);
			setResult(data.text);
		} catch (error) {
			if (error instanceof Object && 'response' in error && (error as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'no_text_found') {
				setResult(t.noText);
			} else {
				setResult(t.error);
			}
		} finally {
			setIsScanning(false);
		}
	}, [webcamRef, language, t.error, t.noText]);

	const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
		if (!e.target.files || e.target.files.length === 0) return;
		const file = e.target.files[0];
		if (!file) return;

		setIsScanning(true);
		try {
			const data = await scanImage(file, language);
			console.log('Data:', data);
			setResult(data.text.join('\n'));
		} catch (error) {
			setResult('Upload failed.');
			console.error('Papyr Upload Error:', error);
		} finally {
			setIsScanning(false);
		}
	};

	const copyToClipboard = () => {
		navigator.clipboard.writeText(result);
		setCopySuccess(true);
		setTimeout(() => setCopySuccess(false), 2000);
	};

	return (
		<div className='min-h-screen w-full flex flex-col items-center py-12 px-6'>
			<div className='fixed top-6 right-6 z-50'>
				<button
					type='button'
					onClick={() => setDarkMode(!darkMode)}
					className={`p-3 rounded-2xl border transition-all active:scale-95 shadow-lg ${
						darkMode
							? 'bg-zinc-900 border-white/10 text-yellow-400 hover:bg-zinc-800'
							: 'bg-white border-zinc-200 text-indigo-600 hover:bg-zinc-50'
					}`}
				>
					{darkMode ? (
						<svg
							xmlns='http://www.w3.org/2000/svg'
							width='20'
							height='20'
							viewBox='0 0 24 24'
							fill='none'
							stroke='currentColor'
							strokeWidth='2'
							strokeLinecap='round'
							strokeLinejoin='round'
						>
							<circle cx='12' cy='12' r='4' />
							<path d='M12 2v2' />
							<path d='M12 20v2' />
							<path d='m4.93 4.93 1.41 1.41' />
							<path d='m17.66 17.66 1.41 1.41' />
							<path d='M2 12h2' />
							<path d='M20 12h2' />
							<path d='m6.34 17.66-1.41 1.41' />
							<path d='m19.07 4.93-1.41 1.41' />
						</svg>
					) : (
						<svg
							xmlns='http://www.w3.org/2000/svg'
							width='20'
							height='20'
							viewBox='0 0 24 24'
							fill='none'
							stroke='currentColor'
							strokeWidth='2'
							strokeLinecap='round'
							strokeLinejoin='round'
						>
							<path d='M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z' />
						</svg>
					)}
				</button>
			</div>

			<div className='w-full max-w-2xl mx-auto flex flex-col items-center py-12 px-6 space-y-10'>
				<header className='text-center space-y-3'>
					<h1
						className={`text-6xl md:text-7xl font-black tracking-tighter italic ${
							darkMode
								? 'bg-linear-to-b from-white to-zinc-500 bg-clip-text text-transparent'
								: 'text-zinc-900'
						}`}
					>
						Papyr
					</h1>
					<p
						className={`${darkMode ? 'text-blue-400' : 'text-blue-600'} font-bold tracking-[0.5em] uppercase text-[10px]`}
					>
						{t.subtitle}
					</p>
				</header>
				<LanguageToggle language={language} setLanguage={setLanguage} />

				<div className='relative w-full aspect-video rounded-[2.5rem] overflow-hidden bg-zinc-900 border border-white/5 shadow-2xl'>
					<Webcam
						ref={webcamRef}
						audio={false}
						screenshotFormat='image/jpeg'
						videoConstraints={videoConstraints}
						onUserMediaError={(err) => console.error('Camera error:', err)}
						className='absolute inset-0 w-full h-full object-cover'
					/>
					{isScanning && <div className='animate-scan z-20' />}
					<div className='absolute top-8 left-8 w-12 h-12 border-t-2 border-l-2 border-white/20 rounded-tl-2xl' />
					<div className='absolute bottom-8 right-8 w-12 h-12 border-b-2 border-r-2 border-white/20 rounded-br-2xl' />{' '}
				</div>

				<div
					className={`w-full max-w-md flex items-center gap-4 p-3 rounded-[2.5rem] border transition-all duration-500 shadow-2xl ${
						darkMode
							? 'bg-zinc-900/90 border-white/10 backdrop-blur-xl'
							: 'bg-white/90 border-zinc-200 backdrop-blur-xl shadow-zinc-200'
					}`}
				>
					<button
						type='button'
						title='Upload'
						onClick={() => fileInputRef.current?.click()}
						className={`p-4 rounded-full transition-all active:scale-90 ${
							darkMode
								? 'text-zinc-400 hover:text-white hover:bg-white/5'
								: 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100'
						}`}
					>
						<Upload size={24} />
					</button>
					<input
						ref={fileInputRef}
						title='Upload'
						type='file'
						accept='image/*'
						onChange={handleFileUpload}
						className='hidden'
					/>
					<button
						onClick={handleCapture}
						type='button'
						disabled={isScanning}
						className={`flex-1 flex items-center justify-center gap-3 py-4 rounded-4xl font-bold text-sm tracking-widest transition-all active:scale-95 disabled:opacity-50 ${
							darkMode
								? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/20'
								: 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-200'
						}`}
					>
						{isScanning ? (
							<>
								<Loader2 className='animate-spin' />
								<span className='uppercase tracking-widest text-[10px]'>
									{t.analyzing}
								</span>
							</>
						) : (
							<>
								<Camera size={22} />
								<span>{t.scanButton}</span>
							</>
						)}
					</button>
				</div>

				{result && (
					<div className='w-full animate-in fade-in slide-in-from-bottom-4 duration-700'>
						<ResultCard
							result={result}
							copySuccess={copySuccess}
							copy={copyToClipboard}
							darkMode={darkMode}
							labels={{
								resultHeader: t.resultHeader,
								copy: t.copy,
								copied: t.copied,
								error: t.error,
								uploadFailed: t.uploadFailed,
								noText: t.noText,
							}}
						/>
					</div>
				)}
			</div>
		</div>
	);
}
