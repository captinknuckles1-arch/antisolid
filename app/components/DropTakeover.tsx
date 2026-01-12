'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

export default function DropTakeover({ edition }: { edition: string }) {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const seen = sessionStorage.getItem(`drop-${edition}`);
    if (seen) setShow(false);
    else {
      sessionStorage.setItem(`drop-${edition}`, 'true');
      setTimeout(() => setShow(false), 2200);
    }
  }, [edition]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.6 }}
          className="fixed inset-0 z-[9999] bg-black flex items-center justify-center"
        >
          <motion.h1
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-white text-4xl tracking-widest uppercase"
          >
            Violent Edition
          </motion.h1>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
