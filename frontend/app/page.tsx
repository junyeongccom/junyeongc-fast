import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">회원 관리 시스템</h1>
      <div className="flex flex-col gap-4">
        <Link 
          href="/dashboard/common/user/templates" 
          className="px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          회원 목록 보기
        </Link>
      </div>
    </main>
  );
} 