import { CheckCircle, Copy } from 'lucide-react';

interface ResultCardProps {
	result: string;
	copySuccess: boolean;
	copy: () => void;
}

export function ResultCard({ result, copySuccess, copy }: ResultCardProps) {
	return (
		<div className='bg-zinc-900/50 backdrop-blur-2xl p-6 rounded-[2rem] border border-white/5 shadow-xl'>
			<div className='flex justify-between items-center mb-4'>
				<h2 className='text-xl font-bold'>Extracted Text</h2>
				<button
					onClick={copy}
					className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300 font-bold text-sm ${
						copySuccess
							? 'bg-green-500/20 text-green-400 border border-green-500/30'
							: 'bg-white/5 text-blue-400 hover:bg-white/10 border border-white/10'
					}`}
				>
					{copySuccess ? (
						<>
							<CheckCircle size={16} />
							Copied!
						</>
					) : (
						<>
							<Copy size={16} />
							Copy Text
						</>
					)}
				</button>
			</div>
			<pre className='whitespace-pre-wrap break-words max-h-[300px] overflow-y-auto'>
				{result}
			</pre>
		</div>
	);
}
