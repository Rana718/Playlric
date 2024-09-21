"use client"
import { Button } from '@/components/ui/button'
import { useRouter } from "next/navigation";
import React from 'react'

function page() {
  const router = useRouter();

  return (
    <div>
      <Button onClick={()=>router.replace("/dashboard")}>start</Button>
    </div>
  )
}

export default page
