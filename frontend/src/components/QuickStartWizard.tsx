import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Cell, Grid } from 'baseui/layout-grid';
import { Button } from 'baseui/button';
import { Input } from 'baseui/input';
import { Block } from 'baseui/block';
import { Check, ChevronRight, ChevronLeft } from 'baseui/icon';
import { Tabs, Tab } from 'baseui/tabs';

type AircraftData = {
  tailNumber: string;
  make: string;
  model: string;
};

type MechanicData = {
  name: string;
  email: string;
  specialties: string[];
};

const headingStyles = {
  h1: {
    fontSize: '28px',
    fontWeight: '700',
    margin: '0 0 8px 0',
  },
  p: {
    fontSize: '14px',
    color: '#666',
    margin: '0',
  },
  h4: {
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '16px',
    margin: '0 0 16px 0',
  },
  h5: {
    fontSize: '16px',
    fontWeight: '600',
    marginBottom: '12px',
    margin: '0 0 12px 0',
  },
};

export default function QuickStartWizard() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [aircraft, setAircraft] = useState<AircraftData[]>([]);
  const [mechanics, setMechanics] = useState<MechanicData[]>([]);
  const [form, setForm] = useState({ tailNumber: '', make: '', model: '' });

  const handleAddAircraft = () => {
    if (form.tailNumber && form.make && form.model) {
      setAircraft([...aircraft, { ...form }]);
      setForm({ tailNumber: '', make: '', model: '' });
    }
  };

  const handleRemoveAircraft = (index: number) => {
    setAircraft(aircraft.filter((_, i) => i !== index));
  };

  const handleAddMechanic = () => {
    // Simple mechanic addition (simplified UI)
    setMechanics([
      ...mechanics,
      {
        name: `Mechanic ${mechanics.length + 1}`,
        email: `mechanic${mechanics.length + 1}@example.com`,
        specialties: ['general'],
      },
    ]);
  };

  const handleRemoveMechanic = (index: number) => {
    setMechanics(mechanics.filter((_, i) => i !== index));
  };

  const handleNext = async () => {
    if (step === 2) {
      // Bulk import data
      const graphName = localStorage.getItem('graphName') || '';
      
      try {
        const response = await fetch(`http://localhost:8080/api/v1/onboard/bulk?graph_name=${graphName}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            aircraft: aircraft,
            mechanics: mechanics,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to import data');
        }

        navigate('/dashboard');
      } catch (err: any) {
        alert(`Error saving data: ${err.message}`);
      }
    } else {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const steps = ['Aircraft', 'Mechanics', 'Review'];

  return (
    <Grid style={{ minHeight: '100vh', background: '#f5f5f5' }}>
      <Cell span={12}>
        <Block
          marginLeft="auto"
          marginRight="auto"
          maxWidth="800px"
          padding="32px"
          marginTop="32px"
          backgroundColor="white"
          borderRadius="8px"
          boxShadow="0 4px 12px rgba(0,0,0,0.1)"
        >
          <Block marginBottom="24px">
            <div style={headingStyles.h1}>Quick Start Wizard</div>
            <div style={headingStyles.p}>Get your SkyMechanics account set up in minutes</div>
          </Block>

          <Tabs
            items={steps}
            activeKey={steps[step]}
            onSelect={(e) => {
              const index = steps.indexOf(e.activeKey as string);
              if (index !== -1) setStep(index);
            }}
          />

          <Block marginTop="32px">
            {step === 0 && (
              <Grid>
                <Cell span={12}>
                  <div style={headingStyles.h4}>Add Aircraft</div>
                  <Grid>
                    <Cell span={4}>
                      <Input
                        label="Tail Number"
                        value={form.tailNumber}
                        onChange={(e) => setForm({ ...form, tailNumber: e.target.value })}
                        placeholder="N12345"
                      />
                    </Cell>
                    <Cell span={4}>
                      <Input
                        label="Make"
                        value={form.make}
                        onChange={(e) => setForm({ ...form, make: e.target.value })}
                        placeholder="Cessna"
                      />
                    </Cell>
                    <Cell span={4}>
                      <Input
                        label="Model"
                        value={form.model}
                        onChange={(e) => setForm({ ...form, model: e.target.value })}
                        placeholder="172"
                      />
                    </Cell>
                  </Grid>
                  <Block marginTop="16px">
                    <Button
                      kind="tertiary"
                      onClick={handleAddAircraft}
                      disabled={!form.tailNumber || !form.make || !form.model}
                    >
                      Add Aircraft
                    </Button>
                  </Block>
                </Cell>
                <Cell span={12} marginTop="24px">
                  <div style={headingStyles.h5}>Added Aircraft ({aircraft.length})</div>
                  {aircraft.length === 0 ? (
                    <div style={headingStyles.p}>No aircraft added yet</div>
                  ) : (
                    <Grid>
                      {aircraft.map((a, i) => (
                        <Cell span={12} key={i}>
                          <Block
                            padding="12px"
                            border="1px solid #ddd"
                            borderRadius="4px"
                            marginBottom="8px"
                            display="flex"
                            justifyContent="space-between"
                            alignItems="center"
                          >
                            <div style={headingStyles.p}>
                              <strong>{a.tailNumber}</strong> - {a.make} {a.model}
                            </div>
                            <Button
                              size="compact"
                              onClick={() => handleRemoveAircraft(i)}
                              kind="negative"
                            >
                              Remove
                            </Button>
                          </Block>
                        </Cell>
                      ))}
                    </Grid>
                  )}
                </Cell>
              </Grid>
            )}

            {step === 1 && (
              <Grid>
                <Cell span={12}>
                  <div style={headingStyles.h4}>Add Mechanics</div>
                  <Button kind="tertiary" onClick={handleAddMechanic}>
                    <Block display="flex" alignItems="center" gap="8px">
                      <Block fontSize="20px">+</Block>
                      Add Mechanic
                    </Block>
                  </Button>
                </Cell>
                <Cell span={12} marginTop="24px">
                  <div style={headingStyles.h5}>Added Mechanics ({mechanics.length})</div>
                  {mechanics.length === 0 ? (
                    <div style={headingStyles.p}>No mechanics added yet</div>
                  ) : (
                    <Grid>
                      {mechanics.map((m, i) => (
                        <Cell span={12} key={i}>
                          <Block
                            padding="12px"
                            border="1px solid #ddd"
                            borderRadius="4px"
                            marginBottom="8px"
                          >
                            <div style={headingStyles.p}>
                              <strong>{m.name}</strong> - {m.email}
                            </div>
                          </Block>
                        </Cell>
                      ))}
                    </Grid>
                  )}
                </Cell>
              </Grid>
            )}

            {step === 2 && (
              <Grid>
                <Cell span={12}>
                  <div style={headingStyles.h4}>Review Your Setup</div>
                  <Block padding="16px" backgroundColor="#f5f5f5" borderRadius="8px" marginBottom="24px">
                    <div style={headingStyles.h5}>Aircraft ({aircraft.length})</div>
                    {aircraft.length === 0 ? (
                      <div style={headingStyles.p}>No aircraft</div>
                    ) : (
                      <ul>
                        {aircraft.map((a, i) => (
                          <li key={i}>
                            <strong>{a.tailNumber}</strong> - {a.make} {a.model}
                          </li>
                        ))}
                      </ul>
                    )}
                  </Block>

                  <Block padding="16px" backgroundColor="#f5f5f5" borderRadius="8px">
                    <div style={headingStyles.h5}>Mechanics ({mechanics.length})</div>
                    {mechanics.length === 0 ? (
                      <div style={headingStyles.p}>No mechanics</div>
                    ) : (
                      <ul>
                        {mechanics.map((m, i) => (
                          <li key={i}>
                            <strong>{m.name}</strong> - {m.email}
                          </li>
                        ))}
                      </ul>
                    )}
                  </Block>
                </Cell>
                <Cell span={12} marginTop="24px">
                  <Block padding="16px" backgroundColor="#e8f4ff" borderRadius="8px">
                    <div style={{ ...headingStyles.p, color: '#1a90ff' }}>
                      <Check size="16px" /> Your data will be saved to the graph database and ready to
                      use!
                    </div>
                  </Block>
                </Cell>
              </Grid>
            )}

            <Block marginTop="32px" display="flex" gap="16px">
              <Button
                kind="secondary"
                disabled={step === 0}
                onClick={handleBack}
                startEnhancer={<ChevronLeft size="24px" />}
              >
                Back
              </Button>
              <Button
                kind="primary"
                onClick={handleNext}
                endEnhancer={<ChevronRight size="24px" />}
              >
                {step === 2 ? 'Finish & Save' : 'Next'}
              </Button>
            </Block>
          </Block>
        </Block>
      </Cell>
    </Grid>
  );
}
