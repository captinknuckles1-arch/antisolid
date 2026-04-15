function pay() {
    const modal = document.createElement('div');
    modal.style = "position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); width:400px; background:#fff; border:2px solid #000; padding:20px; z-index:9999; box-shadow: 10px 10px 0px #000; font-family:monospace;";
    modal.innerHTML = `
        <h3 style="margin-top:0; color:#f00;">⚠️ SECURE WIRE INSTRUCTIONS</h3>
        <p style="font-size:12px;">FORENSIC RECONCILIATION SI-7951-OMEGA</p>
        <hr border="1">
        <div style="background:#eee; padding:10px; font-size:13px; line-height:1.5;">
            <strong>BANK:</strong> JPMORGAN CHASE BANK, N.A.<br>
            <strong>BENEFICIARY:</strong> SOLID INTEGRATIONS LLC<br>
            <strong>ROUTING (ABA):</strong> 021000021<br>
            <strong>ACCOUNT NO:</strong> 2909078106<br>
            <strong>REF:</strong> SI-7951-OMEGA
        </div>
        <p style="font-size:10px; margin-top:15px;">Submit Wire Reference Number once initiated:</p>
        <input type="text" placeholder="REF #" style="width:100%; margin-bottom:10px;">
        <button onclick="this.parentElement.remove()" style="width:100%; background:#000; color:#fff; border:none; padding:10px; cursor:pointer;">CONFIRM INITIATION</button>
    `;
    document.body.appendChild(modal);
}
