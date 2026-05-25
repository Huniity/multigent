import { useState, type FormEvent, type ChangeEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import type { LoginForm, FieldErrors } from '../types/auth';

// Validation
function validate(form: LoginForm): FieldErrors<LoginForm> {
  const errors: FieldErrors<LoginForm> = {};

  if (!form.username.trim()) {
    errors.username = 'Username is required.';
  }

  if (!form.password) {
    errors.password = 'Password is required.';
  } else if (form.password.length < 4) {
    errors.password = 'Password must be at least 4 characters.';
  }

  return errors;
}

// Component
export default function Login() {
  const navigate = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);

  const [form, setForm] = useState<LoginForm>({ username: '', password: '' });
  const [fieldErrors, setFieldErrors] = useState<FieldErrors<LoginForm>>({});
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    // Clears the field error as the user types
    if (fieldErrors[name as keyof LoginForm]) {
      setFieldErrors((prev) => ({ ...prev, [name]: undefined }));
    }
    setApiError(null);
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    const errors = validate(form);
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setLoading(true);
    setApiError(null);

    try {
      const res = await fetch('/api/auth/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: form.username, password: form.password }),
      });

      const data = await res.json();

      if (!res.ok) {
        // Django REST Framework / SimpleJWT error shapes
        if (data.detail) {
          setApiError(data.detail);
        } else if (data.non_field_errors) {
          setApiError((data.non_field_errors as string[])[0]);
        } else {
          // Map field-level errors returned by the API
          const mapped: FieldErrors<LoginForm> = {};
            if (data.username) mapped.username = (data.username as string[])[0];
            if (data.password) mapped.password = (data.password as string[])[0];
            setFieldErrors(mapped);
        }
        return;
      }

      setTokens(data.access as string, data.refresh as string);
      navigate('/');
    } catch {
      setApiError('Unable to connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-1 text-left">
      {/*Brand panel*/}
      <div className="hidden lg:flex flex-col justify-between w-1/2 bg-[#0c0c10] border-r border-[#1a1a22] p-12">
        <Logo />

        <div className="space-y-6">
          <h1 className="font-bold text-4xl leading-tight text-[#f0ede5]"
            style={{ fontFamily: "'Syne', sans-serif" }}>
            Code reviewed<br />by a council<br />of agents.
          </h1>
          <p className="text-sm text-[#787891] leading-relaxed max-w-xs">
            Paste any snippet. Multiple AI agents audit it for security,
            performance, and quality — then produce a single revised output together.
          </p>
        </div>

        <FeatureList />
      </div>

      {/*Form panel*/}
      <div className="flex flex-1 items-center justify-center p-8 bg-[#08080a]">
        <form
          onSubmit={handleSubmit}
          noValidate
          className="w-full max-w-sm space-y-5"
        >
          <div className="mb-8">
            <div className="lg:hidden mb-8"><Logo /></div>
            <h2 className="text-2xl font-bold text-[#f0ede5] mb-1"
              style={{ fontFamily: "'Syne', sans-serif" }}>
              Sign in
            </h2>
            <p className="text-xs text-[#787891]">Welcome back.</p>
          </div>

          {/*API-level error*/}
          {apiError && (
            <div className="text-xs text-[#f87171] bg-[#2a1010] border border-[#f87171]/30 px-4 py-3">
              {apiError}
            </div>
          )}

          <Field
            id="username"
            label="Username"
            type="text"
            name="username"
            placeholder="User123"
            value={form.username}
            onChange={handleChange}
            error={fieldErrors.username}
            autoComplete="username"
          />

          <Field
            id="password"
            label="Password"
            type="password"
            name="password"
            placeholder="••••••••"
            value={form.password}
            onChange={handleChange}
            error={fieldErrors.password}
            autoComplete="current-password"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#aaef5a] text-[#081400] text-xs font-medium tracking-widest uppercase py-3 px-7 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed hover:opacity-85 active:opacity-70 transition-opacity"
          >
            {loading ? 'Signing in…' : '→  Sign in'}
          </button>

          <div className="h-px bg-[#18181e]" />

          <p className="text-xs text-[#787891] text-center">
            No account yet?{' '}
            <Link to="/register" className="text-[#aaef5a] hover:underline">
              Register
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

// Shared sub-components
function Logo() {
  return (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full bg-[#aaef5a]" />
      <span
        className="text-sm font-bold tracking-widest uppercase text-[#f0ede5]"
        style={{ fontFamily: "'Syne', sans-serif" }}
      >
        Multigent
      </span>
    </div>
  );
}

function FeatureList() {
  const items = [
    'Security & vulnerability analysis',
    'Performance & efficiency review',
    'Code quality & maintainability',
    'Unified revised output + agent README',
  ];
  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li key={item} className="flex items-center gap-3">
          <div className="w-1 h-1 rounded-full bg-[#aaef5a] shrink-0" />
          <span className="text-xs text-[#787891]">{item}</span>
        </li>
      ))}
    </ul>
  );
}

interface FieldProps {
  id: string;
  label: string;
  type: string;
  name: string;
  placeholder: string;
  value: string;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  autoComplete?: string;
}

function Field({ id, label, type, name, placeholder, value, onChange, error, autoComplete }: FieldProps) {
  return (
    <div className="space-y-2">
      <label
        htmlFor={id}
        className="block text-[9px] tracking-widest uppercase text-[#787891]"
      >
        {label}
      </label>
      <input
        id={id}
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        autoComplete={autoComplete}
        className={[
          'w-full bg-[#101014] text-[#e2dfda] text-sm px-3.5 py-2.5 outline-none',
          'placeholder:text-[#35333e] font-mono transition-colors',
          'border focus:border-[#aaef5a]',
          error ? 'border-[#f87171]' : 'border-[#20202a]',
        ].join(' ')}
      />
      {error && (
        <span className="block text-[11px] text-[#f87171]">{error}</span>
      )}
    </div>
  );
}
