'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

interface User {
  user_id: string;
  email: string;
  name: string;
}

// 사용자 목록 조회 함수
const fetchUsers = async (): Promise<User[]> => {
  const response = await fetch('http://localhost:8000/customer/list');
  if (!response.ok) {
    throw new Error('사용자 목록을 불러오는데 실패했습니다.');
  }
  const data = await response.json();
  
  // 응답 형식이 변경되었으므로 그에 맞게 처리
  if (data.status === 'error') {
    throw new Error(data.message || '사용자 목록을 불러오는데 실패했습니다.');
  }
  
  return data.data || [];
};

// 사용자 삭제 함수
const deleteUser = async (userId: string): Promise<any> => {
  const response = await fetch(`http://localhost:8000/customer/delete`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId }),
  });
  
  if (!response.ok) {
    throw new Error('사용자 삭제에 실패했습니다.');
  }
  
  return response.json();
};

export default function UserListPage() {
  const queryClient = useQueryClient();
  
  // 사용자 목록 조회 쿼리
  const { data: users, isLoading, isError, error } = useQuery<User[], Error>({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });
  
  // 사용자 삭제 뮤테이션
  const deleteMutation = useMutation({
    mutationFn: deleteUser,
    onSuccess: () => {
      // 삭제 성공 시 사용자 목록 다시 조회
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
  
  // 사용자 삭제 핸들러
  const handleDeleteUser = (userId: string) => {
    if (window.confirm(`정말로 사용자 ID: ${userId}를 삭제하시겠습니까?`)) {
      deleteMutation.mutate(userId);
    }
  };
  
  if (isLoading) {
    return <div className="p-4">사용자 목록을 불러오는 중...</div>;
  }
  
  if (isError) {
    return <div className="p-4 text-red-500">오류 발생: {error.message}</div>;
  }
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">사용자 목록</h1>
      
      {deleteMutation.isPending && (
        <div className="mb-4 p-2 bg-blue-100 text-blue-700 rounded">
          사용자를 삭제하는 중...
        </div>
      )}
      
      {deleteMutation.isError && (
        <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
          삭제 중 오류 발생: {deleteMutation.error.message}
        </div>
      )}
      
      {deleteMutation.isSuccess && (
        <div className="mb-4 p-2 bg-green-100 text-green-700 rounded">
          사용자가 성공적으로 삭제되었습니다.
        </div>
      )}
      
      <table className="min-w-full bg-white border border-gray-200">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b">사용자 ID</th>
            <th className="py-2 px-4 border-b">이메일</th>
            <th className="py-2 px-4 border-b">이름</th>
            <th className="py-2 px-4 border-b">작업</th>
          </tr>
        </thead>
        <tbody>
          {users && users.length > 0 ? (
            users.map((user) => (
              <tr key={user.user_id} className="hover:bg-gray-50">
                <td className="py-2 px-4 border-b">{user.user_id}</td>
                <td className="py-2 px-4 border-b">{user.email}</td>
                <td className="py-2 px-4 border-b">{user.name}</td>
                <td className="py-2 px-4 border-b">
                  <button
                    onClick={() => handleDeleteUser(user.user_id)}
                    className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded"
                    disabled={deleteMutation.isPending}
                  >
                    삭제
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={4} className="py-4 px-4 text-center">
                사용자가 없습니다.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
} 