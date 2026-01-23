import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, Upload, Loader2 } from 'lucide-react';
import { scanImage } from './services/api';
import { ResultCard } from './components/Result';
import LanguageToggle from './components/LanguageToggle';

const videoConstraints = {
	width: { min: 640, ideal: 960, max: 2560 }, // High-definition capture
	height: { min: 360, ideal: 540, max: 1440 },
	facingMode: 'environment',
	focusMode: 'continuous', // Critical for sharp text
};

export default function App() {
	const webcamRef = useRef<Webcam>(null);
	const fileInputRef = useRef<HTMLInputElement>(null);
	const [result, setResult] = useState('');
	const [isScanning, setIsScanning] = useState(false);
	const [copySuccess, setCopySuccess] = useState(false);
	const [language, setLanguage] = useState('en');

	// Convert Base64 from Webcam to Blob for API consumption
	const handleCapture = useCallback(async () => {
		if (!webcamRef.current) return;
		const imageSrc = webcamRef.current.getScreenshot();
		if (!imageSrc) return;

		setIsScanning(true);
		try {
			const blob = await fetch(imageSrc).then((r) => r.blob());
			const data = await scanImage(blob);
			console.log('Data:', data.data);
			setResult(data.data.join('\n'));
		} catch (error) {
			console.error('Papyr Error:', error);
			setResult('Error: Could not connect to the engine.');
		} finally {
			setIsScanning(false);
		}
	}, [webcamRef]);

	const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
		if (!e.target.files || e.target.files.length === 0) return;
		const file = e.target.files[0];
		if (!file) return;

		setIsScanning(true);
		try {
			const data = await scanImage(file);
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
		<div className='w-full flex flex-col items-center py-12 px-4 min-h-screen'>
			<div className='w-full max-w-2xl flex flex-col items-center text-center space-y-8'>
				<header className='text-center space-y-2'>
					<h1 className='text-5xl md:text-6xl font-black tracking-tighter bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent pb-1'>
						Papyr
					</h1>
					<p className='text-zinc-500 font-medium tracking-[0.3em] uppercase text-[10px]'>
						Neural Book Digitization
					</p>
				</header>

				<LanguageToggle language={language} setLanguage={setLanguage} />

				<div className='relative w-full aspect-video rounded-[2.5rem] overflow-hidden border border-white/10 bg-black shadow-2xl'>
					<Webcam
						ref={webcamRef}
						audio={false}
						screenshotFormat='image/jpeg'
						videoConstraints={videoConstraints}
						className='absolute inset-0 w-full h-full object-cover'
					/>

					{isScanning && <div className='animate-scan z-10' />}
					<div className='absolute top-6 left-6 w-10 h-10 border-t-2 border-l-2 border-white/20 rounded-tl-xl pointer-events-none' />
					<div className='absolute bottom-6 right-6 w-10 h-10 border-b-2 border-r-2 border-white/20 rounded-br-xl pointer-events-none' />
				</div>

				<div className='w-full flex items-center justify-center gap-4 bg-zinc-900/80 backdrop-blur-xl p-3 rounded-[2rem] border border-white/10 shadow-xl'>
					<button
						type='button'
						title='Upload'
						onClick={() => fileInputRef.current?.click()}
						className='p-4 text-zinc-400 hover:text-white transition-colors'
					>
						<Upload size={24} />
					</button>

					{/* THE TRIPLE-LOCK HIDDEN INPUT 
              This prevents "Choose File" from appearing in any browser 
          */}
					<input
						ref={fileInputRef}
						title='Upload'
						type='file'
						onChange={handleFileUpload}
						style={{
							display: 'none',
						}}
					/>

					<button
						onClick={handleCapture}
						type='button'
						disabled={isScanning}
						className='flex-1 flex items-center justify-center gap-3 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl font-bold text-lg shadow-lg active:scale-95 transition-all disabled:opacity-50'
					>
						{isScanning ? (
							<Loader2 className='animate-spin' />
						) : (
							<Camera size={22} />
						)}
						{isScanning ? 'Processing...' : 'Scan Page'}
					</button>
				</div>

				{/* Results: ensure they take the full width of the centered column */}
				{result && (
					<div className='w-full max-w-2xl'>
						<ResultCard
							result={result}
							copySuccess={copySuccess}
							copy={copyToClipboard}
						/>
					</div>
				)}
			</div>
		</div>
	);
}
