export default function LanguageToggle({
	language,
	setLanguage,
}: {
	language: string;
	setLanguage: (language: string) => void;
}) {
	return (
		<div className='flex items-center gap-2'>
			<button
				onClick={() => setLanguage('en')}
				className={`px-4 py-2 rounded-lg transition-colors ${
					language === 'en'
						? 'bg-blue-600 text-white'
						: 'bg-zinc-800 text-zinc-400'
				}`}
			>
				English
			</button>
			<button
				onClick={() => setLanguage('vi')}
				className={`px-4 py-2 rounded-lg transition-colors ${
					language === 'vi'
						? 'bg-blue-600 text-white'
						: 'bg-zinc-800 text-zinc-400'
				}`}
			>
				Vietnamese
			</button>
		</div>
	);
}
